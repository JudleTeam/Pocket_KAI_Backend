from datetime import datetime

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


if TYPE_CHECKING:
    from database.models import PocketKAIUser


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    token: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str | None] = mapped_column()
    is_revoked: Mapped[bool] = mapped_column(default=False)

    issued_at: Mapped[datetime] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column()
    last_used_at: Mapped[datetime | None] = mapped_column()
    revoked_at: Mapped[datetime | None] = mapped_column()

    pocket_kai_user_id: Mapped[UUID] = mapped_column(ForeignKey('pocket_kai_user.id'))

    pocket_kai_user: Mapped['PocketKAIUser'] = relationship(
        back_populates='refresh_tokens',
    )
