from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from api.dependencies import ScheduleServiceDep
from api.kai.schemas.schedule import DayResponse, WeekDaysResponse
from core.entities.lesson import WeekParity
from core.exceptions.base import EntityNotFoundError


router = APIRouter()


@router.get(
    '/group/by_name/{group_name}/schedule/week',
    response_model=WeekDaysResponse,
)
async def get_week_schedule_by_group_name(
    group_name: str,
    week_parity: Annotated[WeekParity, Query()] = WeekParity.any,
    *,
    schedule_service: ScheduleServiceDep
):
    try:
        return await schedule_service.get_schedule_with_week_days_by_group_name(group_name, week_parity=week_parity)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    '/group/by_id/{group_id}/schedule/week',
    response_model=WeekDaysResponse
)
async def get_week_schedule_by_group_id(
    group_id: UUID,
    week_parity: Annotated[WeekParity, Query()] = WeekParity.any,
    *,
    schedule_service: ScheduleServiceDep
):
    try:
        return await schedule_service.get_schedule_with_week_days_by_group_id(group_id, week_parity=week_parity)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    '/group/by_id/{group_id}/schedule/',
    response_model=list[DayResponse]
)
async def get_schedule_with_dates_by_group_id(
    date_from: Annotated[date, Query(default_factory=date.today, description='By default is today')],
    group_id: UUID,
    days: Annotated[int, Query(ge=1, le=31)] = 7,
    *,
    schedule_service: ScheduleServiceDep
):
    try:
        return await schedule_service.get_schedule_with_dates_by_group_id(
            group_id=group_id, date_from=date_from, days_count=days
        )
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    '/group/by_name/{group_name}/schedule/',
    response_model=list[DayResponse]
)
async def get_schedule_with_dates_by_group_name(
    date_from: Annotated[date, Query(default_factory=date.today, description='By default is today')],
    group_name: str,
    days: Annotated[int, Query(ge=1, le=31)] = 7,
    *,
    schedule_service: ScheduleServiceDep
):
    try:
        return await schedule_service.get_schedule_with_dates_by_group_name(
            group_name=group_name, date_from=date_from, days_count=days
        )
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
