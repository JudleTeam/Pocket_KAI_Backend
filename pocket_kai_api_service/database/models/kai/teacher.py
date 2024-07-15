from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseModel


class TeacherModel(BaseModel):
    __tablename__ = 'teacher'

    login: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
