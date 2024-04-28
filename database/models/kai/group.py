from uuid import UUID

from sqlalchemy import Column, BigInteger, Integer, select, ForeignKey, Text, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
import sqlalchemy as sa

from database.base import Base


class Group(Base):
    __tablename__ = 'group'

    kai_id:             Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    group_leader_id:    Mapped[UUID] = mapped_column(ForeignKey('kai_user.id'), nullable=True)
    pinned_text:        Mapped[str] = mapped_column(nullable=True)
    group_name:         Mapped[int] = mapped_column(nullable=False, unique=True)

    syllabus_url:               Mapped[str] = mapped_column(nullable=True)
    educational_program_url:    Mapped[str] = mapped_column(nullable=True)
    study_schedule_url:         Mapped[str] = mapped_column(nullable=True)

    speciality_id:  Mapped[UUID] = mapped_column(ForeignKey('speciality.id'), nullable=True)
    profile_id:     Mapped[UUID] = mapped_column(ForeignKey('profile.id'), nullable=True)
    institute_id:   Mapped[UUID] = mapped_column(ForeignKey('institute.id'), nullable=True)
    departament_id: Mapped[UUID] = mapped_column(ForeignKey('departament.id'), nullable=True)

    speciality:     Mapped['Speciality'] = relationship('Speciality', lazy='selectin')
    profile:        Mapped['Profile'] = relationship('Profile', lazy='selectin')
    departament:    Mapped['Departament'] = relationship('Departament', lazy='selectin')
    institute:      Mapped['Institute'] = relationship('Institute', lazy='selectin')

    group_leader: Mapped['KAIUser'] = relationship('KAIUser', foreign_keys=[group_leader_id])
    members: Mapped[list['KAIUser']] = relationship('KAIUser', back_populates='group', foreign_keys='[KAIUser.group_id]')

    @classmethod
    async def get_group_by_name(cls, session, group_name):
        if isinstance(group_name, str) and not group_name.isdigit():
            return None

        record = await session.execute(select(Group).where(Group.group_name == int(group_name)))
        return record.scalar()

    @classmethod
    async def get_all(cls, session):
        stmt = select(Group)
        records = await session.execute(stmt)
        return records.scalars().all()
