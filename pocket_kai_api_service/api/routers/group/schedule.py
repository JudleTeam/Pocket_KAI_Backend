from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from api.dependencies import ScheduleServiceDep
from api.schemas.common import ErrorMessage
from api.schemas.schedule import ScheduleResponse, WeekDaysResponse
from core.entities.lesson import WeekParity
from core.exceptions.base import EntityNotFoundError

router = APIRouter()


@router.get(
    '/by_name/{group_name}/schedule/week',
    response_model=WeekDaysResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model'      : ErrorMessage
        }
    }
)
async def get_week_schedule_by_group_name(
    group_name: str,
    week_parity: Annotated[WeekParity, Query()] = WeekParity.any,
    *,
    schedule_service: ScheduleServiceDep
):
    """
    Возвращает расписание по дням недели без конкретных дат для группы по её имени (номеру).
    Можно передать чётность недели. Пары, у которых чётность определилась как чёт/неч, возвращаются *всегда*
    """
    try:
        return await schedule_service.get_schedule_with_week_days_by_group_name(group_name, week_parity=week_parity)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    '/by_id/{group_id}/schedule/week',
    response_model=WeekDaysResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model'      : ErrorMessage
        }
    }
)
async def get_week_schedule_by_group_id(
    group_id: UUID,
    week_parity: Annotated[WeekParity, Query()] = WeekParity.any,
    *,
    schedule_service: ScheduleServiceDep
):
    """
    Возвращает расписание по дням недели без конкретных дат для группы по её имени (номеру).
    Можно передать чётность недели. Пары, у которых чётность определилась как чёт/неч, возвращаются *всегда*
    """
    try:
        return await schedule_service.get_schedule_with_week_days_by_group_id(group_id, week_parity=week_parity)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    '/by_id/{group_id}/schedule/',
    response_model=ScheduleResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model'      : ErrorMessage
        }
    }
)
async def get_schedule_with_dates_by_group_id(
    date_from: Annotated[date, Query(default_factory=date.today, description='By default is today')],
    group_id: UUID,
    days_count: Annotated[int, Query(ge=1, le=31)] = 7,
    *,
    schedule_service: ScheduleServiceDep
):
    """
    Возвращает список дней с парами для группы по её ID (ID из PocketKAI).
    Дни начинаются с дня переданного в параметре `date_from` (по умолчанию это будет текущий день),
    количество дней в списке зависит от параметра `days_count`
    """
    try:
        return await schedule_service.get_schedule_with_dates_by_group_id(
            group_id=group_id, date_from=date_from, days_count=days_count
        )
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    '/by_name/{group_name}/schedule/',
    response_model=ScheduleResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model'      : ErrorMessage
        }
    }
)
async def get_schedule_with_dates_by_group_name(
    date_from: Annotated[date, Query(default_factory=date.today, description='By default is today')],
    group_name: str,
    days_count: Annotated[int, Query(ge=1, le=31)] = 7,
    *,
    schedule_service: ScheduleServiceDep
):
    """
    Возвращает список дней с парами для группы по её имени (номеру).
    Дни начинаются с дня переданного в параметре `date_from` (по умолчанию это будет текущий день),
    количество дней в списке зависит от параметра `days_count`
    """
    try:
        return await schedule_service.get_schedule_with_dates_by_group_name(
            group_name=group_name, date_from=date_from, days_count=days_count
        )
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
