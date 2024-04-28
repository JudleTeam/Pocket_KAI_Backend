from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy as sa

from database.base import Base


class Speciality(Base):
    __tablename__ = 'speciality'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    code:   Mapped[str] = mapped_column(nullable=False)
    name:   Mapped[str] = mapped_column(nullable=False)

    @classmethod
    async def get_or_create(cls, session, spec_id: int, name: str, code: str):
        spec = await session.get(Speciality, spec_id)
        if not spec:
            spec = Speciality(id=spec_id, name=name, code=code)
            session.add(spec)

        return spec
