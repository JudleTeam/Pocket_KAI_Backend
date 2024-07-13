from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa

from database.models.base import BaseModel


class SpecialityModel(BaseModel):
    __tablename__ = 'speciality'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    code: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
