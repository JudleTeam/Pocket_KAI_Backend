import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base


class Discipline(Base):
    __tablename__ = 'discipline'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    name: Mapped[str] = mapped_column()
