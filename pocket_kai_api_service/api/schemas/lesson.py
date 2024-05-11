import datetime
from typing import Annotated
from uuid import UUID
import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from api.schemas.department import DepartmentRead
from api.schemas.discipline import DisciplineRead
from api.schemas.teacher import TeacherRead
from core.entities.lesson import LessonType, WeekParity


class LessonRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    created_at: datetime.datetime
    group_id: UUID
    number_of_day: int
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[dt.date] | None
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType
    start_time: dt.time
    end_time: dt.time | None

    teacher: TeacherRead | None
    department: DepartmentRead
    discipline: DisciplineRead


class LessonCreate(BaseModel):
    number_of_day: Annotated[int, Field(ge=1, le=7)]
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[dt.date] | None
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType | None
    start_time: dt.time
    end_time: dt.time | None
    discipline_id: UUID
    teacher_id: UUID | None
    department_id: UUID
    group_id: UUID


class LessonUpdate(BaseModel):
    number_of_day: Annotated[int, Field(ge=1, le=7)]
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[dt.date] | None
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType | None
    start_time: dt.time
    end_time: dt.time | None
    discipline_id: UUID
    teacher_id: UUID | None
    department_id: UUID
    group_id: UUID
