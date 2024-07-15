import datetime

from typing import Annotated

from fastapi import APIRouter, Query

from api.schemas.common import WeekParityResponse
from core.entities.common import WeekParity


router = APIRouter()


@router.get(
    '/week_parity',
    response_model=WeekParityResponse,
)
async def get_week_parity(
    date: Annotated[
        datetime.date,
        Query(
            default_factory=datetime.date.today,
            title='Дата',
            description='Дата для получения четности. По умолчанию - сегодня',
        ),
    ],
):
    """
    Возвращает чётность недели по дате.
    """
    parity = WeekParity.get_parity_for_date(date)
    return WeekParityResponse(
        date=date,
        parity=parity,
        int_parity=parity.to_int(),
    )
