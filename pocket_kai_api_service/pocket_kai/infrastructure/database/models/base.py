from datetime import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa


class BaseModel(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    @classmethod
    async def get_or_create(
        cls,
        session: AsyncSession,
        defaults=None,
        commit=True,
        **kwargs,
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
