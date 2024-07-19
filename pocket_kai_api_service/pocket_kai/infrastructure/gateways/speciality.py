from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.speciality import (
    SpecialityReader,
    SpecialitySaver,
)
from pocket_kai.domain.entitites.speciality import SpecialityEntity
from pocket_kai.infrastructure.database.models.kai import SpecialityModel


class SpecialityGateway(SpecialityReader, SpecialitySaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def db_to_entity(
        speciality_record: SpecialityModel | None,
    ) -> SpecialityEntity | None:
        if not speciality_record:
            return None

        return SpecialityEntity(
            id=speciality_record.id,
            created_at=speciality_record.created_at,
            kai_id=speciality_record.kai_id,
            name=speciality_record.name,
            code=speciality_record.code,
        )

    async def get_by_kai_id(self, kai_id: int) -> SpecialityEntity | None:
        return self.db_to_entity(
            await self._session.scalar(
                select(SpecialityModel).where(SpecialityModel.kai_id == kai_id),
            ),
        )

    async def get_by_id(self, id: str) -> SpecialityEntity | None:
        return self.db_to_entity(
            await self._session.get(SpecialityModel, id),
        )

    async def save(self, speciality: SpecialityEntity) -> None:
        await self._session.execute(
            insert(SpecialityModel).values(
                id=speciality.id,
                created_at=speciality.created_at,
                kai_id=speciality.kai_id,
                code=speciality.code,
                name=speciality.name,
            ),
        )
