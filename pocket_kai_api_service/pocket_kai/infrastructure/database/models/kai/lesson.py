from datetime import date, time
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ARRAY, ForeignKey, Date
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, Mapped, mapped_column

from pocket_kai.infrastructure.database.models.base import BaseModel


if TYPE_CHECKING:
    from pocket_kai.infrastructure.database.models.kai import (
        DepartmentModel,
        DisciplineModel,
        GroupModel,
        TeacherModel,
    )


class LessonModel(BaseModel):
    __tablename__ = 'lesson'

    number_of_day: Mapped[int] = mapped_column()
    original_dates: Mapped[str | None] = mapped_column()
    parsed_parity: Mapped[str] = mapped_column()
    parsed_dates: Mapped[list[date] | None] = mapped_column(
        MutableList.as_mutable(ARRAY(Date)),
    )
    parsed_dates_status: Mapped[str] = mapped_column()
    audience_number: Mapped[str | None] = mapped_column()
    building_number: Mapped[str | None] = mapped_column()
    original_lesson_type: Mapped[str | None] = mapped_column()
    parsed_lesson_type: Mapped[str] = mapped_column()
    start_time: Mapped[time | None] = mapped_column()
    end_time: Mapped[time | None] = mapped_column()

    discipline_id: Mapped[UUID] = mapped_column(ForeignKey('discipline.id'))
    department_id: Mapped[UUID | None] = mapped_column(ForeignKey('department.id'))
    teacher_id: Mapped[UUID | None] = mapped_column(ForeignKey('teacher.id'))
    group_id: Mapped[UUID] = mapped_column(ForeignKey('group.id'))

    department: Mapped[Optional['DepartmentModel']] = relationship()
    discipline: Mapped['DisciplineModel'] = relationship()
    # Если teacher = None, значит стоит "Преподаватель кафедры"
    teacher: Mapped[Optional['TeacherModel']] = relationship()
    group: Mapped['GroupModel'] = relationship()

    def __repr__(self):
        return f'{self.original_dates} | {self.start_time.strftime("%H:%M")} | {self.discipline.name}'
