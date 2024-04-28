from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa

from database.base import Base


class Profile(Base):
    __tablename__ = 'profile'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    name:   Mapped[str] = mapped_column(nullable=False)

    @classmethod
    async def get_or_create(cls, session, prof_id: int, name: str):
        prof = await session.get(Profile, prof_id)
        if not prof:
            prof = Profile(id=prof_id, name=name)
            session.add(prof)

        return prof
