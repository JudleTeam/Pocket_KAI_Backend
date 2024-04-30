import os
from datetime import date
from typing import TYPE_CHECKING
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

if TYPE_CHECKING:
    from database.models import PocketKAIUser
    from database.models.kai import Group


settings = get_settings()


class KAIUser(Base):
    __tablename__ = 'kai_user'

    kai_id:     Mapped[int | None] = mapped_column(sa.BigInteger, unique=True)

    position:   Mapped[int | None] = mapped_column()
    login:      Mapped[str | None] = mapped_column(unique=True)
    password:   Mapped[str | None] = mapped_column(StringEncryptedType(key=settings.SECRET_KEY))
    full_name:  Mapped[str] = mapped_column()
    phone:      Mapped[str | None] = mapped_column(unique=False)  # Бывает что у двух людей один и тот же номер!
    email:      Mapped[str] = mapped_column(unique=True)
    sex:        Mapped[str | None] = mapped_column()
    birthday:   Mapped[date | None] = mapped_column()
    is_leader:  Mapped[bool] = mapped_column()

    zach_number:        Mapped[str | None] = mapped_column()  # Уникальный?
    competition_type:   Mapped[str | None] = mapped_column()
    contract_number:    Mapped[int | None] = mapped_column(sa.BigInteger)  # Уникальный?
    edu_level:          Mapped[str | None] = mapped_column()
    edu_cycle:          Mapped[str | None] = mapped_column()
    edu_qualification:  Mapped[str | None] = mapped_column()
    program_form:       Mapped[str | None] = mapped_column()
    status:             Mapped[str | None] = mapped_column()

    group_id:           Mapped[UUID] = mapped_column(ForeignKey('group.id', name='fk_kai_user_group'))
    pocket_kai_user_id: Mapped[UUID] = mapped_column(ForeignKey('pocket_kai_user.id'), unique=True)

    group: Mapped['Group'] = relationship(foreign_keys=[group_id], back_populates='members')
    pocket_kai_user: Mapped['PocketKAIUser'] = relationship(back_populates='kai_user')

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

