from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class ProfileBase(BaseModel):
    kai_id: int
    name: str


class ProfileRead(ProfileBase):
    id: UUID
    created_at: datetime
