from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class SpecialityBase(BaseModel):
    name: str
    kai_id: int
    code: str


class SpecialityRead(SpecialityBase):
    id: UUID
    created_at: datetime
