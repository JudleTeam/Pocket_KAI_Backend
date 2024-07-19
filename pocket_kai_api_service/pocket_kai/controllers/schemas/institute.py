from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class InstituteBase(BaseModel):
    kai_id: int
    name: str


class InstituteRead(InstituteBase):
    id: UUID
    created_at: datetime
