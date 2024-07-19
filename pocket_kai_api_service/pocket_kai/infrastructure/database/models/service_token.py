from sqlalchemy.orm import Mapped, mapped_column

from pocket_kai.infrastructure.database.models.base import BaseModel


class ServiceTokenModel(BaseModel):
    __tablename__ = 'service_token'

    token: Mapped[str] = mapped_column(unique=True)
