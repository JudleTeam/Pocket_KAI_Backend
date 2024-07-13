from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import StringEncryptedType
import sqlalchemy as sa

from config import get_settings
from database.models.base import BaseModel

if TYPE_CHECKING:
    from database.models import UserModel
    from database.models.kai import GroupModel


settings = get_settings()


class StudentModel(BaseModel):
    __tablename__ = 'student'

    kai_id: Mapped[int | None] = mapped_column(sa.BigInteger, unique=True)

    position: Mapped[int | None] = mapped_column()
    login: Mapped[str | None] = mapped_column(unique=True)
    password: Mapped[str | None] = mapped_column(
        StringEncryptedType(key=settings.SECRET_KEY),
    )
    full_name: Mapped[str] = mapped_column()
    phone: Mapped[str | None] = mapped_column(
        unique=False,
    )  # Бывает что у двух людей один и тот же номер!
    email: Mapped[str] = mapped_column(unique=True)
    sex: Mapped[str | None] = mapped_column()
    birthday: Mapped[date | None] = mapped_column()
    is_leader: Mapped[bool] = mapped_column()

    zach_number: Mapped[str | None] = mapped_column()  # Уникальный?
    competition_type: Mapped[str | None] = mapped_column()
    contract_number: Mapped[str | None] = mapped_column()  # Уникальный?
    edu_level: Mapped[str | None] = mapped_column()
    edu_cycle: Mapped[str | None] = mapped_column()
    edu_qualification: Mapped[str | None] = mapped_column()
    program_form: Mapped[str | None] = mapped_column()
    status: Mapped[str | None] = mapped_column()

    group_id: Mapped[UUID] = mapped_column(
        ForeignKey('group.id', name='fk_student_group'),
    )
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('user.id'),
        unique=True,
    )

    group: Mapped['GroupModel'] = relationship(
        foreign_keys=[group_id],
        back_populates='members',
    )
    user: Mapped['UserModel'] = relationship(back_populates='student')
