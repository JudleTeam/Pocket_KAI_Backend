import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Departament(Base):
    __tablename__ = 'departament'

    kai_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    @property
    def short_name(self):
        name_parts = self.name.title().split()
        short_name = ''
        for ind, part in enumerate(name_parts):
            if part.lower() == 'кафедра':
                continue

            if part.lower() == 'и':
                if not (len(name_parts) - 1 > ind > 0 and name_parts[ind + 1].lower()[0] != 'и' and name_parts[ind - 1].lower()[0] != 'и'):
                    continue

                short_name += 'и'
                continue

            if part.lower() == 'как':
                if not (len(name_parts) - 1 > ind > 0 and name_parts[ind + 1].lower()[0] != 'к' and name_parts[ind - 1].lower()[0] != 'к'):
                    continue

                short_name += 'к'
                continue

            short_name += part[0]

        return short_name
