from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class TeacherBase(BaseModel):
    login: str
    name: str


class TeacherRead(TeacherBase):
    id: UUID
    created_at: datetime


class TeacherCreate(TeacherBase): ...
