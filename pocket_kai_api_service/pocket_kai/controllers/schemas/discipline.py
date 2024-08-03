from datetime import datetime

from uuid import UUID

from pydantic import BaseModel

from pocket_kai.controllers.schemas.teacher import TeacherRead
from pocket_kai.domain.common import LessonType


class DisciplineBase(BaseModel):
    kai_id: int
    name: str


class DisciplineRead(DisciplineBase):
    id: UUID
    created_at: datetime


class DisciplineCreate(DisciplineBase):
    pass


class DisciplineTypeWithTeacherResponse(BaseModel):
    parsed_type: LessonType
    original_type: str
    teacher: TeacherRead | None


class DisciplineWithTypesResponse(BaseModel):
    id: UUID
    kai_id: int
    name: str
    types: list[DisciplineTypeWithTeacherResponse]
