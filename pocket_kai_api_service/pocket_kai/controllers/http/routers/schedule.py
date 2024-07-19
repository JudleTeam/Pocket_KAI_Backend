from datetime import date
from dishka import FromDishka

from uuid import UUID

from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Query, status

from pocket_kai.application.interactors.schedule import (
    GetDatesScheduleByGroupIdInteractor,
    GetDatesScheduleByGroupNameInteractor,
    GetWeekScheduleByGroupIdInteractor,
    GetWeekScheduleByGroupNameInteractor,
)
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.schedule import ScheduleResponse, WeekDaysResponse
from pocket_kai.domain.common import WeekParity
from pocket_kai.domain.exceptions.group import GroupNotFoundError


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '/by_name/{group_name}/schedule/week',
    response_model=WeekDaysResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model': ErrorMessage,
        },
    },
)
async def get_week_schedule_by_group_name(
    group_name: str,
    week_parity: Annotated[WeekParity, Query()] = WeekParity.ANY,
    *,
    interactor: FromDishka[GetWeekScheduleByGroupNameInteractor],
):
    """
    Возвращает расписание по дням недели без конкретных дат для группы по её имени (номеру).
    Можно передать чётность недели. Пары, у которых чётность определилась как чёт/неч, возвращаются *всегда*
    """
    try:
        return await interactor(
            group_name,
            week_parity=week_parity,
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )


@router.get(
    '/by_id/{group_id}/schedule/week',
    response_model=WeekDaysResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model': ErrorMessage,
        },
    },
)
async def get_week_schedule_by_group_id(
    group_id: UUID,
    week_parity: Annotated[WeekParity, Query()] = WeekParity.ANY,
    *,
    interactor: FromDishka[GetWeekScheduleByGroupIdInteractor],
):
    """
    Возвращает расписание по дням недели без конкретных дат для группы по её имени (номеру).
    Можно передать чётность недели. Пары, у которых чётность определилась как чёт/неч, возвращаются *всегда*
    """
    try:
        return await interactor(
            group_id,
            week_parity=week_parity,
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )


@router.get(
    '/by_id/{group_id}/schedule/',
    response_model=ScheduleResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model': ErrorMessage,
        },
    },
)
async def get_schedule_with_dates_by_group_id(
    date_from: Annotated[
        date,
        Query(default_factory=date.today, description='By default is today'),
    ],
    group_id: UUID,
    days_count: Annotated[int, Query(ge=1, le=31)] = 7,
    *,
    interactor: FromDishka[GetDatesScheduleByGroupIdInteractor],
):
    """
    Возвращает список дней с парами для группы по её ID (ID из PocketKAI).
    Дни начинаются с дня переданного в параметре `date_from` (по умолчанию это будет текущий день),
    количество дней в списке зависит от параметра `days_count`.
    Если у пары есть список `parsed_dates`, то пара вернётся только если день с парой попадает в этот список.
    """
    try:
        return await interactor(
            group_id=group_id,
            date_from=date_from,
            days_count=days_count,
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )


@router.get(
    '/by_name/{group_name}/schedule/',
    response_model=ScheduleResponse,
    responses={
        404: {
            'description': 'Group not found',
            'model': ErrorMessage,
        },
    },
)
async def get_schedule_with_dates_by_group_name(
    date_from: Annotated[
        date,
        Query(default_factory=date.today, description='By default is today'),
    ],
    group_name: str,
    days_count: Annotated[int, Query(ge=1, le=31)] = 7,
    *,
    interactor: FromDishka[GetDatesScheduleByGroupNameInteractor],
):
    """
    Возвращает список дней с парами для группы по её имени (номеру).
    Дни начинаются с дня переданного в параметре `date_from` (по умолчанию это будет текущий день),
    количество дней в списке зависит от параметра `days_count`.
    Если у пары есть список `parsed_dates`, то пара вернётся только если день с парой попадает в этот список.
    """
    try:
        return await interactor(
            group_name=group_name,
            date_from=date_from,
            days_count=days_count,
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )
