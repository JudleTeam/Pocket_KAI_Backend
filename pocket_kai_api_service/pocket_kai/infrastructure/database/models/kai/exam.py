from typing import Optional, TYPE_CHECKING
import datetime as dt

from sqlalchemy import ForeignKey
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from pocket_kai.infrastructure.database.models.base import BaseModel


if TYPE_CHECKING:
    from pocket_kai.infrastructure.database.models.kai import (
        DisciplineModel,
        GroupModel,
        TeacherModel,
    )


class ExamModel(BaseModel):
    __tablename__ = 'exam'

    original_date: Mapped[str] = mapped_column()
    time: Mapped[dt.time] = mapped_column()

    audience_number: Mapped[str | None] = mapped_column()
    building_number: Mapped[str | None] = mapped_column()
    parsed_date: Mapped[dt.date | None] = mapped_column()
    academic_year: Mapped[str] = mapped_column()
    academic_year_half: Mapped[int] = mapped_column()
    semester: Mapped[int | None] = mapped_column()

    discipline_id: Mapped[UUID] = mapped_column(ForeignKey('discipline.id'))
    teacher_id: Mapped[UUID | None] = mapped_column(ForeignKey('teacher.id'))
    group_id: Mapped[UUID] = mapped_column(ForeignKey('group.id'))

    discipline: Mapped['DisciplineModel'] = relationship()
    # Если teacher = None, значит стоит "Преподаватель кафедры"
    teacher: Mapped[Optional['TeacherModel']] = relationship()
    group: Mapped['GroupModel'] = relationship()
