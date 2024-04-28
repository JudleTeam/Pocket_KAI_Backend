from datetime import time
from uuid import UUID

from sqlalchemy import select, delete, ForeignKey, or_
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import Base


class GroupLesson(Base):
    __tablename__ = 'group_lesson'

    number_of_day:          Mapped[int] = mapped_column(nullable=False)
    parity_of_week:         Mapped[str] = mapped_column(nullable=True)
    int_parity_of_week:     Mapped[int] = mapped_column(nullable=False)
    auditory_number:        Mapped[str] = mapped_column(nullable=True)
    building_number:        Mapped[str] = mapped_column(nullable=True)
    lesson_type:            Mapped[str] = mapped_column(nullable=True)
    start_time:             Mapped[time] = mapped_column(nullable=False)
    end_time:               Mapped[time] = mapped_column(nullable=True)

    discipline_id:  Mapped[UUID] = mapped_column(ForeignKey('discipline.id'), nullable=False)
    teacher_id:     Mapped[UUID] = mapped_column(ForeignKey('teacher.id'), nullable=True)
    group_id:       Mapped[UUID] = mapped_column(ForeignKey('group.id'), nullable=False)

    discipline: Mapped['Discipline'] = relationship('Discipline', lazy='selectin', backref='lessons')
    # Если teacher = None, значит стоит "Преподаватель кафедры"
    teacher: Mapped['Teacher'] = relationship('Teacher', backref='lessons', lazy='selectin')
    group: Mapped['Group'] = relationship('Group', backref='lessons', lazy='selectin')

    def __repr__(self):
        return f'{self.parity_of_week} | {self.start_time.strftime("%H:%M")} | {self.discipline.name}'

    @classmethod
    async def get_group_day_schedule(cls, session, group_id, day, int_parity: int = 0):
        stmt = select(GroupLesson).where(
            GroupLesson.group_id == group_id,
            GroupLesson.number_of_day == day,
            or_(
                GroupLesson.int_parity_of_week == 0,
                GroupLesson.int_parity_of_week == int_parity
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

    @classmethod
    async def update_or_create(cls, session, group_id: int, lesson, discipline, teacher, int_parity, end_time):
        stmt = select(GroupLesson).where(
            GroupLesson.group_id == group_id,
            GroupLesson.number_of_day == lesson.dayNum,
            GroupLesson.start_time == lesson.dayTime,
            GroupLesson.teacher == teacher,
            GroupLesson.discipline == discipline,
            GroupLesson.int_parity_of_week == int_parity
        )
        record = await session.execute(stmt)
        db_lesson: GroupLesson = record.scalar()

        if db_lesson:
            db_lesson.parity_of_week = lesson.dayDate
            db_lesson.lesson_type = lesson.disciplType
            db_lesson.auditory_number = lesson.audNum
            db_lesson.building_number = lesson.buildNum
            db_lesson.end_time = end_time
        else:
            db_lesson = GroupLesson(
                group_id=group_id,
                number_of_day=lesson.dayNum,
                parity_of_week=lesson.dayDate,
                int_parity_of_week=int_parity,
                discipline=discipline,
                auditory_number=lesson.audNum,
                building_number=lesson.buildNum,
                lesson_type=lesson.disciplType,
                start_time=lesson.dayTime,
                end_time=end_time,
                teacher=teacher
            )
            session.add(db_lesson)

        return db_lesson
