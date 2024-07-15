from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseModel


class TaskModel(BaseModel):
    __tablename__ = 'task'

    name: Mapped[str] = mapped_column()

    type: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()

    login: Mapped[str | None] = mapped_column()
    group_name: Mapped[str | None] = mapped_column()

    errors: Mapped[str | None] = mapped_column()

    ended_at: Mapped[datetime | None] = mapped_column()
