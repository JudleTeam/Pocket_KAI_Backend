from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from database.base import Base


class PocketKAIUser(Base):
    __tablename__ = 'pocket_kai_user'

    telegram_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)

    is_blocked: Mapped[bool] = mapped_column(default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    last_activity: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    tokens = relationship('Token', back_populates='pocket_kai_user', foreign_keys='[Token.pocket_kai_user_id]')
    kai_user = relationship('KAIUser', back_populates='pocket_kai_user', foreign_keys='[KAIUser.pocket_kai_user_id]')
