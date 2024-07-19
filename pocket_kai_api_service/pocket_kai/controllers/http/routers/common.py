import datetime

from typing import Annotated

from fastapi import APIRouter, Query

from pocket_kai.controllers.schemas.common import WeekParityResponse
from pocket_kai.domain.common import WeekParity


router = APIRouter()


@router.get(
    '/week_parity',
    response_model=WeekParityResponse,
    name='Получить четность недели по дате',
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
