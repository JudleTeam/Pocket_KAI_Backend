from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa

from pocket_kai.infrastructure.database.models.base import BaseModel


class InstituteModel(BaseModel):
    __tablename__ = 'institute'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    name: Mapped[str] = mapped_column()
