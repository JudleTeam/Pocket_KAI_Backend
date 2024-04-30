from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa

from database.base import Base


class Institute(Base):
    __tablename__ = 'institute'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    name:   Mapped[str] = mapped_column()
