import dataclasses
from datetime import datetime


@dataclasses.dataclass(slots=True)
class RefreshTokenEntity:
    id: str
    created_at: datetime
    token: str
    name: str | None
    is_revoked: bool

    issued_at: datetime
    expires_at: datetime
    last_used_at: datetime | None
    revoked_at: datetime | None

    user_id: str
