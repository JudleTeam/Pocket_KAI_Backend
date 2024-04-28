from uuid import UUID

from sqlalchemy import Column, String, Integer, ForeignKey, text, select, func, or_
from sqlalchemy.orm import relationship, Mapped, mapped_column
import sqlalchemy as sa

from database.base import Base


class Teacher(Base):
    __tablename__ = 'teacher'

    login: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=False)

    departament_id: Mapped[UUID] = mapped_column(ForeignKey('departament.id'))

    departament: Mapped['Departament'] = relationship('Departament', lazy='selectin', backref='teachers')

    @classmethod
    async def search_by_name(cls, session, name, similarity=0.3, limit=50, offset=0):
        await session.execute(text('CREATE EXTENSION IF NOT EXISTS pg_trgm'))
        name = name.lower()
        records = await session.execute(
            select(Teacher).where(
                or_(func.similarity(Teacher.name, name) > similarity, Teacher.name.ilike(f'%{name}%'))
            ).limit(limit).offset(offset)
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
