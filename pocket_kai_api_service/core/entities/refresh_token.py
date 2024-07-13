from uuid import UUID

from datetime import datetime

from core.entities.base import BaseEntity


class RefreshTokenEntity(BaseEntity):
    token: str
    name: str | None
    is_revoked: bool

    issued_at: datetime
    expires_at: datetime
    last_used_at: datetime | None
    revoked_at: datetime | None

    pocket_kai_user_id: UUID
