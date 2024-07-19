from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int | None
    phone: str | None
    is_blocked: bool


class UserRead(UserBase):
    id: UUID
    created_at: datetime
