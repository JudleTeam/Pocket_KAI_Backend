from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class DisciplineBase(BaseModel):
    kai_id: int
    name: str


class DisciplineRead(DisciplineBase):
    id: UUID
    created_at: datetime


class DisciplineCreate(DisciplineBase):
    pass
