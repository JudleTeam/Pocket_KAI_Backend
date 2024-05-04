from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class ServiceToken(Base):
    __tablename__ = 'service_token'

    token: Mapped[str] = mapped_column()
