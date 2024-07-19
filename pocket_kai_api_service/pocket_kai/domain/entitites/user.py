from datetime import datetime

import dataclasses


@dataclasses.dataclass(slots=True)
class UserEntity:
    id: str
    created_at: datetime
    telegram_id: int | None
    phone: str | None
    is_blocked: bool
