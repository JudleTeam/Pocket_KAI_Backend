import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from pocket_kai.infrastructure.database.models.base import BaseModel


class DisciplineModel(BaseModel):
    __tablename__ = 'discipline'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    name: Mapped[str] = mapped_column()
