import datetime as dt
from enum import Enum
from typing import Annotated, Union
from uuid import UUID

from pydantic import Field

from core.entities.base import BaseEntity
from core.entities.discipline import DisciplineEntity
from core.entities.teacher import TeacherEntity


class LessonType(str, Enum):
    lecture = 'lecture'
    practice = 'practice'
    laboratory_work = 'lab_work'
    consultation = 'consult'
    physical_education = 'phys_edu'
    course_work = 'course_work'
    individual_task = 'ind_task'
    unknown = 'unknown'


class WeekParity(str, Enum):
    odd = 'odd'
    even = 'even'
    any = 'any'

    @classmethod
    def get_parity_for_date(cls, date: dt.date) -> Union['WeekParity.even', 'WeekParity.odd']:
        if int(date.strftime("%V")) % 2 == 1:
            return cls.odd
        return cls.even


class LessonEntity(BaseEntity):
    number_of_day: Annotated[int, Field(ge=1, le=7, description='Monday - 1, ..., Sunday - 7')]
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[dt.date] | None

    start_time: dt.time
    end_time: dt.time | None

    audience_number: str | None
    building_number: str | None

    original_lesson_type: str | None
    parsed_lesson_type: LessonType

    parsed_at: dt.datetime

    group_id: UUID

    discipline: DisciplineEntity
    teacher: TeacherEntity | None
