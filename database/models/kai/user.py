import os
from datetime import date
from uuid import UUID

from dotenv import load_dotenv
from sqlalchemy import Integer, Column, BigInteger, ForeignKey, String, Date, Boolean
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import StringEncryptedType
import sqlalchemy as sa

from config import get_settings
from database.base import Base

settings = get_settings()


class KAIUser(Base):
    __tablename__ = 'kai_user'

    kai_id:     Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=True)

    position:   Mapped[int] = mapped_column(nullable=True)
    login:      Mapped[str] = mapped_column(unique=True, nullable=True)
    password:   Mapped[str] = mapped_column(StringEncryptedType(key=settings.SECRET_KEY), nullable=True)
    full_name:  Mapped[str] = mapped_column(nullable=False)
    phone:      Mapped[str] = mapped_column(nullable=True, unique=False)  # Бывает что у двух людей один и тот же номер!
    email:      Mapped[str] = mapped_column(nullable=False, unique=True)
    sex:        Mapped[str] = mapped_column(nullable=True)
    birthday:   Mapped[date] = mapped_column(nullable=True)
    is_leader:  Mapped[bool] = mapped_column(nullable=False)

    zach_number:        Mapped[str] = mapped_column(nullable=True)  # Уникальный?
    competition_type:   Mapped[str] = mapped_column(nullable=True)
    contract_number:    Mapped[int] = mapped_column(sa.BigInteger, nullable=True)  # Уникальный?
    edu_level:          Mapped[str] = mapped_column(nullable=True)
    edu_cycle:          Mapped[str] = mapped_column(nullable=True)
    edu_qualification:  Mapped[str] = mapped_column(nullable=True)
    program_form:       Mapped[str] = mapped_column(nullable=True)
    status:             Mapped[str] = mapped_column(nullable=True)

    group_id:           Mapped[UUID] = mapped_column(ForeignKey('group.id', name='fk_kai_user_group'), nullable=False)
    pocket_kai_user_id: Mapped[UUID] = mapped_column(ForeignKey('pocket_kai_user.id'), unique=True)

    group: Mapped['Group'] = relationship('Group', foreign_keys=[group_id], back_populates='members')
    pocket_kai_user: Mapped['PocketKAIUser'] = relationship('PocketKAIUser', back_populates='kai_user')

    async def get_classmates(self, db: async_sessionmaker):
        async with db() as session:
            records = await session.execute(select(KAIUser).where(KAIUser.group_id == self.group_id).order_by(KAIUser.position))

        return records.scalars().all()

    @property
    def is_logged_in(self) -> bool:
        return bool(self.kai_id)

    @classmethod
    async def get_by_phone(cls, phone: str, db: async_sessionmaker):
        async with db() as session:
            records = await session.execute(select(KAIUser).where(KAIUser.phone == phone))

        return records.scalars().all()

    @classmethod
    async def get_by_email(cls, session, email: str):
        record = await session.execute(select(KAIUser).where(KAIUser.email == email))

        return record.scalar()

