from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


if TYPE_CHECKING:
    from database.models import PocketKAIUser


class Token(Base):
    __tablename__ = 'token'

    token: Mapped[str] = mapped_column(unique=True)
    pocket_kai_user_id: Mapped[UUID] = mapped_column(ForeignKey('pocket_kai_user.id'))

    pocket_kai_user: Mapped['PocketKAIUser'] = relationship(back_populates='tokens')
