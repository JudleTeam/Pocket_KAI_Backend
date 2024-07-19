import datetime as dt

import dataclasses

from pocket_kai.application.dto.lesson import LessonExtendedDTO
from pocket_kai.domain.common import WeekParity


@dataclasses.dataclass(slots=True)
class DayDTO:
    date: dt.date
    parity: WeekParity
    lessons: list[LessonExtendedDTO]


@dataclasses.dataclass(slots=True)
class ScheduleDTO:
    parsed_at: dt.datetime | None
    days: list[DayDTO]


@dataclasses.dataclass(slots=True)
class WeekDTO:
    monday: list[LessonExtendedDTO]
    tuesday: list[LessonExtendedDTO]
    wednesday: list[LessonExtendedDTO]
    thursday: list[LessonExtendedDTO]
    friday: list[LessonExtendedDTO]
    saturday: list[LessonExtendedDTO]
    sunday: list[LessonExtendedDTO]


@dataclasses.dataclass(slots=True)
class WeekDaysDTO:
    parsed_at: dt.datetime | None
    week_parity: WeekParity
    week_days: WeekDTO
