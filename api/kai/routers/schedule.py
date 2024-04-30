from datetime import date
from enum import Enum
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Query

from api.dependencies import ScheduleServiceDep
from core.services.schedule import DayResponse


router = APIRouter()


class ParityEnum(Enum):
    Any = 0
    Odd = 1
    Even = 2


@router.get(
    '/group/{group_name}/schedule/week'
)
async def get_week_schedule_by_group_name(
    group_name: str,
    parity: Annotated[ParityEnum, Query()] = ParityEnum.Any,
):
    example = {
        'parity': parity,
        'schedule': {
            'monday': [

            ],
            'tuesday': [

            ],
            'wednesday': [

            ],
            'thursday': [

            ],
            'friday': [

            ],
            'saturday': [

            ]
        }
    }


@router.get(
    '/group/{group_id}/schedule/',
    response_model=list[DayResponse]
)
async def get_group_schedule_with_dates_by_group_id(
    date_from: Annotated[date, Query(default_factory=date.today, description='By default is today')],
    group_id: UUID,
    days: Annotated[int, Query(ge=1, le=31)] = 7,
    *,
    schedule_service: ScheduleServiceDep
):
    return await schedule_service.get_group_schedule_with_dates(
        group_id=group_id, date_from=date_from, days=days
    )
