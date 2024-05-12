import datetime as dt
from typing import Annotated
from uuid import UUID

from pydantic import Field

from core.entities.base import BaseEntity
from core.entities.common import LessonType, ParsedDatesStatus, WeekParity
from core.entities.department import DepartmentEntity
from core.entities.discipline import DisciplineEntity
from core.entities.teacher import TeacherEntity


class LessonEntity(BaseEntity):
    number_of_day: Annotated[int, Field(ge=1, le=7, description='Monday - 1, ..., Sunday - 7')]
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[dt.date] | None
    parsed_dates_status: ParsedDatesStatus

    start_time: dt.time
    end_time: dt.time | None

    audience_number: str | None
    building_number: str | None

    original_lesson_type: str | None
    parsed_lesson_type: LessonType

    group_id: UUID
    discipline_id: UUID
    teacher_id: UUID | None

    discipline: DisciplineEntity = None
    teacher: TeacherEntity | None = None
    department: DepartmentEntity = None
