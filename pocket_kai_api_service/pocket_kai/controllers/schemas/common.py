from enum import Enum

from typing import Annotated

import datetime

from pydantic import BaseModel, Field


class ErrorMessage(BaseModel):
    detail: str


class WeekParityWithoutAny(str, Enum):
    ODD = 'odd'  # Нечётная
    EVEN = 'even'  # Чётная


class WeekParityResponse(BaseModel):
    date: datetime.date
    parity: WeekParityWithoutAny
    int_parity: Annotated[
        int,
        Field(
            ge=0,
            le=1,
            title='Чётность недели числом',
            description='Чётность недели числом. 0 - четная, 1 - нечетная',
        ),
    ]
