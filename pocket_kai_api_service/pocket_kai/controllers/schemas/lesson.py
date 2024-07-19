from uuid import UUID

from datetime import date, datetime, time

from typing import Annotated

from pydantic import BaseModel, Field

from pocket_kai.controllers.schemas.department import DepartmentRead
from pocket_kai.controllers.schemas.discipline import DisciplineRead
from pocket_kai.controllers.schemas.teacher import TeacherRead
from pocket_kai.domain.common import LessonType, ParsedDatesStatus, WeekParity


class LessonBase(BaseModel):
    number_of_day: Annotated[int, Field(ge=1, le=7)]
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[date] | None
    parsed_dates_status: ParsedDatesStatus
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType | None
    start_time: time | None
    end_time: time | None


class LessonRead(LessonBase):
    id: UUID
    created_at: datetime
    group_id: UUID

    teacher: TeacherRead | None
    department: DepartmentRead | None
    discipline: DisciplineRead


class LessonCreate(LessonBase):
    discipline_id: UUID
    teacher_id: str | None
    department_id: str | None
    group_id: str


class LessonUpdate(LessonBase):
    created_at: datetime
    discipline_id: UUID
    teacher_id: UUID | None
    department_id: UUID | None
    group_id: UUID
