import datetime as dt

from pydantic import BaseModel, ConfigDict

from core.entities.lesson import LessonEntity, WeekParity


class DayEntity(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    date: dt.date
    parity: WeekParity = WeekParity.any
    lessons: list[LessonEntity]


class Week(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    monday: list[LessonEntity]
    tuesday: list[LessonEntity]
    wednesday: list[LessonEntity]
    thursday: list[LessonEntity]
    friday: list[LessonEntity]
    saturday: list[LessonEntity]
    sunday: list[LessonEntity]


class WeekEntity(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    week_parity: WeekParity
    week_days: Week
