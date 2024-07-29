from uuid import UUID
import datetime as dt

from pydantic import BaseModel

from pocket_kai.controllers.schemas.discipline import DisciplineRead
from pocket_kai.controllers.schemas.teacher import TeacherRead


class ExamBase(BaseModel):
    original_date: str
    time: dt.time
    audience_number: str | None
    building_number: str | None
    parsed_date: dt.date | None
    academic_year: str
    academic_year_half: int
    semester: int | None
    discipline_id: UUID
    teacher_id: UUID | None
    group_id: UUID


class ExamCreate(ExamBase): ...


class ExamUpdate(ExamBase):
    created_at: dt.datetime


class ExamRead(ExamBase):
    id: UUID
    created_at: dt.datetime

    teacher: TeacherRead
    discipline: DisciplineRead
