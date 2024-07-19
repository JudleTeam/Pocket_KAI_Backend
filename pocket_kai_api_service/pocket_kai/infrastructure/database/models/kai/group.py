from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
import sqlalchemy as sa

from pocket_kai.infrastructure.database.models.base import BaseModel


if TYPE_CHECKING:
    from pocket_kai.infrastructure.database.models.kai import (
        SpecialityModel,
        ProfileModel,
        DepartmentModel,
        InstituteModel,
        StudentModel,
    )


class GroupModel(BaseModel):
    __tablename__ = 'group'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    group_leader_id: Mapped[UUID | None] = mapped_column(ForeignKey('student.id'))
    pinned_text: Mapped[str | None] = mapped_column()
    group_name: Mapped[str] = mapped_column(unique=True)

    is_verified: Mapped[bool] = mapped_column(default=False)
    verified_at: Mapped[datetime | None] = mapped_column(default=None)
    # Дата последнего парсинга именно для верифицированной группы, т.е. обновление участников и остального
    parsed_at: Mapped[datetime | None] = mapped_column(default=None)

    schedule_parsed_at: Mapped[datetime | None] = mapped_column(default=None)

    syllabus_url: Mapped[str | None] = mapped_column()
    educational_program_url: Mapped[str | None] = mapped_column()
    study_schedule_url: Mapped[str | None] = mapped_column()

    speciality_id: Mapped[UUID | None] = mapped_column(ForeignKey('speciality.id'))
    profile_id: Mapped[UUID | None] = mapped_column(ForeignKey('profile.id'))
    institute_id: Mapped[UUID | None] = mapped_column(ForeignKey('institute.id'))
    department_id: Mapped[UUID | None] = mapped_column(ForeignKey('department.id'))

    speciality: Mapped['SpecialityModel'] = relationship(lazy='selectin')
    profile: Mapped['ProfileModel'] = relationship(lazy='selectin')
    department: Mapped['DepartmentModel'] = relationship(lazy='selectin')
    institute: Mapped['InstituteModel'] = relationship(lazy='selectin')

    group_leader: Mapped['StudentModel'] = relationship(foreign_keys=[group_leader_id])
    members: Mapped[list['StudentModel']] = relationship(
        back_populates='group',
        foreign_keys='[StudentModel.group_id]',
    )
