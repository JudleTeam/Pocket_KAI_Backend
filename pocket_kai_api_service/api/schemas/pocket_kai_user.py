from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class PocketKaiUserRead(BaseModel):
    id: UUID
    created_at: datetime
    telegram_id: int | None
    phone: str | None
    is_blocked: bool
