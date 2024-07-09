import datetime as dt

from pydantic import BaseModel, ConfigDict

from api.schemas.lesson import LessonRead
from core.entities.common import WeekParity


class ScheduleLesson(LessonRead):
    groups_on_stream: list[str]


class ScheduleResponse(BaseModel):
    parsed_at: dt.datetime | None
    days: list['DayResponse']


class DayResponse(BaseModel):
    date: dt.date
    parity: WeekParity = WeekParity.any
    lessons: list[ScheduleLesson]


class WeekResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    monday: list[ScheduleLesson]
    tuesday: list[ScheduleLesson]
    wednesday: list[ScheduleLesson]
    thursday: list[ScheduleLesson]
    friday: list[ScheduleLesson]
    saturday: list[ScheduleLesson]
    sunday: list[ScheduleLesson]


class WeekDaysResponse(BaseModel):
    parsed_at: dt.datetime | None
    week_parity: WeekParity
    week_days: WeekResponse
