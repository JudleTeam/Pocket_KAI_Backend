from datetime import datetime
from uuid import UUID

from api.schemas.common import TunedModel


class UserRead(TunedModel):
    id: UUID
    created_at: datetime
    telegram_id: int | None
    phone: str | None
    is_blocked: bool
