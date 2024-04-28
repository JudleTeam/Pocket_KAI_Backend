from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa

from database.base import Base


class Institute(Base):
    __tablename__ = 'institute'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    name:   Mapped[str] = mapped_column(nullable=False)

    @classmethod
    async def get_or_create(cls, session, inst_id: int, name: str):
        inst = await session.get(Institute, inst_id)
        if not inst:
            inst = Institute(id=inst_id, name=name)
            session.add(inst)

        return inst
