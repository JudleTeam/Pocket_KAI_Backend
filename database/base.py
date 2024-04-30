import uuid
from datetime import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa

from config import get_settings


settings = get_settings()
engine = create_async_engine(settings.database_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    @classmethod
    async def get_or_create(
            cls, session: AsyncSession, defaults=None, commit=True, **kwargs
    ) -> tuple[Self, bool]:
        """Django-inspired get_or_create."""
        predicates = [getattr(cls, k) == v for k, v in kwargs.items()]
        instance = await session.scalar(sa.select(cls).where(*predicates))
        if instance:
            return instance, False

        defaults = defaults or {}
        instance_kwargs = kwargs | defaults
        instance = cls(**instance_kwargs)
        session.add(instance)
        if commit:
            await session.commit()

        return instance, True


async def get_async_session():
    async with async_session_maker() as session:
        yield session
