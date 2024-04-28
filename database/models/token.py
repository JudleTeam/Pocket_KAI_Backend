from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Token(Base):
    __tablename__ = 'token'

    token: Mapped[str] = mapped_column(unique=True, nullable=False)
    pocket_kai_user_id: Mapped[UUID] = mapped_column(ForeignKey('pocket_kai_user.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    pocket_kai_user: Mapped['PocketKAIUser'] = relationship('PocketKAIUser', back_populates='tokens')
