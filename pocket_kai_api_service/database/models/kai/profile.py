from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa

from database.models.base import BaseModel


class ProfileModel(BaseModel):
    __tablename__ = 'profile'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    name: Mapped[str] = mapped_column()
