from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from database.models.base import Base


if TYPE_CHECKING:
    from database.models import RefreshToken
    from database.models.kai import KAIUser


class PocketKAIUser(Base):
    __tablename__ = 'pocket_kai_user'

    telegram_id: Mapped[int | None] = mapped_column(
        sa.BigInteger,
        unique=True,
        default=None,
    )

    phone: Mapped[str | None] = mapped_column(unique=True, default=None)

    is_blocked: Mapped[bool] = mapped_column(default=False)

    refresh_tokens: Mapped['RefreshToken'] = relationship(
        back_populates='pocket_kai_user',
        foreign_keys='[RefreshToken.pocket_kai_user_id]',
    )
    kai_user: Mapped['KAIUser'] = relationship(
        back_populates='pocket_kai_user',
        foreign_keys='[KAIUser.pocket_kai_user_id]',
    )
