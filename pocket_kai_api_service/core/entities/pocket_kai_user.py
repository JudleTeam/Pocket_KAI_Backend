from core.entities.base import BaseEntity


class PocketKaiUserEntity(BaseEntity):
    telegram_id: int | None
    phone: str | None
    is_blocked: bool
