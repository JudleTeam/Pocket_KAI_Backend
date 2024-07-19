from datetime import datetime

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from pocket_kai.infrastructure.database.models.base import BaseModel


if TYPE_CHECKING:
    from pocket_kai.infrastructure.database.models import UserModel


class RefreshTokenModel(BaseModel):
    __tablename__ = 'refresh_token'

    token: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str | None] = mapped_column()
    is_revoked: Mapped[bool] = mapped_column(default=False)

    issued_at: Mapped[datetime] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column()
    last_used_at: Mapped[datetime | None] = mapped_column()
    revoked_at: Mapped[datetime | None] = mapped_column()

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))

    user: Mapped['UserModel'] = relationship(
        back_populates='refresh_tokens',
    )
