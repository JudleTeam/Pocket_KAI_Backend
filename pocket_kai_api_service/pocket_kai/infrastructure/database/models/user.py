from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa


from pocket_kai.infrastructure.database.models.base import BaseModel


if TYPE_CHECKING:
    from pocket_kai.infrastructure.database.models import RefreshTokenModel
    from pocket_kai.infrastructure.database.models.kai import StudentModel


class UserModel(BaseModel):
    __tablename__ = 'user'

    telegram_id: Mapped[int | None] = mapped_column(
        sa.BigInteger,
        unique=True,
        default=None,
    )

    phone: Mapped[str | None] = mapped_column(unique=True, default=None)

    is_blocked: Mapped[bool] = mapped_column(default=False)

    refresh_tokens: Mapped['RefreshTokenModel'] = relationship(
        back_populates='user',
        foreign_keys='[RefreshTokenModel.user_id]',
    )
    student: Mapped['StudentModel'] = relationship(
        back_populates='user',
        foreign_keys='[StudentModel.user_id]',
    )
