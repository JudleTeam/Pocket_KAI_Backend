from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, text, select, func, or_
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.models.base import Base

if TYPE_CHECKING:
    from database.models.kai import Department


class Teacher(Base):
    __tablename__ = 'teacher'

    login: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()

    department_id: Mapped[UUID | None] = mapped_column(ForeignKey('department.id'))

    department: Mapped[Optional['Department']] = relationship(lazy='selectin')

    @classmethod
    async def search_by_name(cls, session, name, similarity=0.3, limit=50, offset=0):
        await session.execute(text('CREATE EXTENSION IF NOT EXISTS pg_trgm'))
        name = name.lower()
        records = await session.execute(
            select(Teacher)
            .where(
                or_(
                    func.similarity(Teacher.name, name) > similarity,
                    Teacher.name.ilike(f'%{name}%'),
                ),
            )
            .limit(limit)
            .offset(offset),
        )
        return records.scalars().all()

    @property
    def short_name(self):
        name_parts = self.name.split()
        letters = [f'{part[0]}.' for part in name_parts[1:]]
        short_name = f'{name_parts[0]} {"".join(letters)}'

        return short_name

    def __repr__(self):
        return f'{self.name} | {self.login}'
