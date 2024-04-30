from datetime import UTC, date, datetime, time
from functools import partial
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ARRAY, select, delete, ForeignKey, or_, Date
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import Base


if TYPE_CHECKING:
    from database.models.kai import Discipline, Teacher, Group


class GroupLesson(Base):
    __tablename__ = 'group_lesson'

    number_of_day:           Mapped[int] = mapped_column()
    original_dates:          Mapped[str | None] = mapped_column()
    parsed_parity:           Mapped[str] = mapped_column()
    parsed_dates:            Mapped[list[date] | None] = mapped_column(MutableList.as_mutable(ARRAY(Date)))
    audience_number:         Mapped[str | None] = mapped_column()
    building_number:         Mapped[str | None] = mapped_column()
    original_lesson_type:    Mapped[str | None] = mapped_column()
    parsed_lesson_type:      Mapped[str] = mapped_column()
    start_time:              Mapped[time] = mapped_column()
    end_time:                Mapped[time | None] = mapped_column()

    discipline_id:  Mapped[UUID] = mapped_column(ForeignKey('discipline.id'))
    teacher_id:     Mapped[UUID | None] = mapped_column(ForeignKey('teacher.id'))
    group_id:       Mapped[UUID] = mapped_column(ForeignKey('group.id'))

    parsed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    discipline: Mapped['Discipline'] = relationship(lazy='selectin')
    # Если teacher = None, значит стоит "Преподаватель кафедры"
    teacher: Mapped[Optional['Teacher']] = relationship(lazy='selectin')
    group: Mapped['Group'] = relationship(lazy='selectin')

    def __repr__(self):
        return f'{self.original_dates} | {self.start_time.strftime("%H:%M")} | {self.discipline.name}'

    @classmethod
    async def get_group_day_schedule(cls, session, group_id, day, int_parity: int = 0):
        stmt = select(GroupLesson).where(
            GroupLesson.group_id == group_id,
            GroupLesson.number_of_day == day,
            or_(
                GroupLesson.parsed_parity == 0,
                GroupLesson.parsed_parity == int_parity
            )
        ).order_by(GroupLesson.start_time)

        records = await session.execute(stmt)
        return records.scalars().all()

    @classmethod
    async def get_group_day_schedule_with_any_parity(cls, session, group_id, day):
        stmt = select(GroupLesson).where(
            GroupLesson.group_id == group_id,
            GroupLesson.number_of_day == day
        ).order_by(GroupLesson.start_time)

        records = await session.execute(stmt)
        return records.scalars().all()

    @classmethod
    async def get_group_schedule(cls, session, group_id):
        stmt = select(GroupLesson).where(
            GroupLesson.group_id == group_id
        )

        records = await session.execute(stmt)
        return records.scalars().all()

    @classmethod
    async def get_teacher_schedule(cls, session, teacher_login):
        stmt = (select(GroupLesson)
                .where(GroupLesson.teacher_id == teacher_login).
                order_by(GroupLesson.number_of_day, GroupLesson.start_time))

        records = await session.execute(stmt)
        return records.scalars().all()

    @classmethod
    async def clear_group_schedule(cls, session, group_id):
        stmt = delete(GroupLesson).where(GroupLesson.group_id == group_id)
        await session.execute(stmt)

    @classmethod
    async def clear_old_schedule(cls, session, group_id: int, new_schedule: list) -> list:
        deleted_lessons = list()
        current_schedule = await cls.get_group_schedule(session, group_id)
        for old_lesson in current_schedule:
            if old_lesson not in new_schedule:
                deleted_lessons.append(old_lesson)
                await session.refresh(old_lesson, ['homework'])
                old_lesson.homework = []
                await session.delete(old_lesson)

        return deleted_lessons
