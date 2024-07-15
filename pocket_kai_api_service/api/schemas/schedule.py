import datetime as dt

from api.schemas.common import TunedModel
from api.schemas.lesson import LessonRead
from core.entities.common import WeekParity


class ScheduleResponse(TunedModel):
    parsed_at: dt.datetime | None
    days: list['DayResponse']


class DayResponse(TunedModel):
    date: dt.date
    parity: WeekParity = WeekParity.ANY
    lessons: list[LessonRead]


class Week(TunedModel):
    monday: list[LessonRead]
    tuesday: list[LessonRead]
    wednesday: list[LessonRead]
    thursday: list[LessonRead]
    friday: list[LessonRead]
    saturday: list[LessonRead]
    sunday: list[LessonRead]


class WeekDaysResponse(TunedModel):
    parsed_at: dt.datetime | None
    week_parity: WeekParity
    week_days: Week
