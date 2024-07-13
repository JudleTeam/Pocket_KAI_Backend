from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.models.base import BaseModel

if TYPE_CHECKING:
    from database.models.kai import DepartmentModel


class TeacherModel(BaseModel):
    __tablename__ = 'teacher'

    login: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()

    department_id: Mapped[UUID | None] = mapped_column(ForeignKey('department.id'))

    department: Mapped[Optional['DepartmentModel']] = relationship(lazy='selectin')
