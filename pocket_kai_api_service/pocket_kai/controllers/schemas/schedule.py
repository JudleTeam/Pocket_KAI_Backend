import datetime as dt
from pydantic import BaseModel

from pocket_kai.controllers.schemas.lesson import LessonRead
from pocket_kai.domain.common import WeekParity


class ScheduleResponse(BaseModel):
    parsed_at: dt.datetime | None
    days: list['DayResponse']


class DayResponse(BaseModel):
    date: dt.date
    parity: WeekParity = WeekParity.ANY
    lessons: list[LessonRead]


class Week(BaseModel):
    monday: list[LessonRead]
    tuesday: list[LessonRead]
    wednesday: list[LessonRead]
    thursday: list[LessonRead]
    friday: list[LessonRead]
    saturday: list[LessonRead]
    sunday: list[LessonRead]


class WeekDaysResponse(BaseModel):
    parsed_at: dt.datetime | None
    week_parity: WeekParity
    week_days: Week
