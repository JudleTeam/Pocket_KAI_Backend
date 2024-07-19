from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class DepartmentBase(BaseModel):
    kai_id: int
    name: str


class DepartmentRead(DepartmentBase):
    id: UUID
    created_at: datetime


class DepartmentCreate(DepartmentBase):
    pass
