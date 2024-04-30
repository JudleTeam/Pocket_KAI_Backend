from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
import sqlalchemy as sa

from database.base import Base


if TYPE_CHECKING:
    from database.models.kai import Speciality, Profile, Department, Institute, KAIUser


class Group(Base):
    __tablename__ = 'group'

    kai_id:             Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    group_leader_id:    Mapped[UUID | None] = mapped_column(ForeignKey('kai_user.id'))
    pinned_text:        Mapped[str | None] = mapped_column()
    group_name:         Mapped[str] = mapped_column(unique=True)

    is_verified: Mapped[bool] = mapped_column(default=False)
    verified_at: Mapped[datetime | None] = mapped_column(default=None)
    # Дата последнего парсинга именно для верифицированной группы, т.е. обновление участников и остального
    parsed_at:  Mapped[datetime | None] = mapped_column(default=None)

    syllabus_url:               Mapped[str | None] = mapped_column()
    educational_program_url:    Mapped[str | None] = mapped_column()
    study_schedule_url:         Mapped[str | None] = mapped_column()

    speciality_id:  Mapped[UUID | None] = mapped_column(ForeignKey('speciality.id'))
    profile_id:     Mapped[UUID | None] = mapped_column(ForeignKey('profile.id'))
    institute_id:   Mapped[UUID | None] = mapped_column(ForeignKey('institute.id'))
    department_id: Mapped[UUID | None] = mapped_column(ForeignKey('department.id'))

    speciality:     Mapped['Speciality'] = relationship(lazy='selectin')
    profile:        Mapped['Profile'] = relationship(lazy='selectin')
    departament:    Mapped['Department'] = relationship(lazy='selectin')
    institute:      Mapped['Institute'] = relationship(lazy='selectin')

    group_leader: Mapped['KAIUser'] = relationship(foreign_keys=[group_leader_id])
    members: Mapped[list['KAIUser']] = relationship(back_populates='group', foreign_keys='[KAIUser.group_id]')
