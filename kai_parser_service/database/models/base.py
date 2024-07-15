from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
