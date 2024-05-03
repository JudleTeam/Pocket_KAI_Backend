import datetime as dt

from pydantic import BaseModel, ConfigDict

from api.kai.schemas.lesson import LessonRead
from core.entities.lesson import WeekParity


class DayResponse(BaseModel):
    date: dt.date
    parity: WeekParity = WeekParity.any
    lessons: list[LessonRead]


class Week(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    monday: list[LessonRead]
    tuesday: list[LessonRead]
    wednesday: list[LessonRead]
    thursday: list[LessonRead]
    friday: list[LessonRead]
    saturday: list[LessonRead]
    sunday: list[LessonRead]


class WeekDaysResponse(BaseModel):
    parity: WeekParity
    week_days: Week
