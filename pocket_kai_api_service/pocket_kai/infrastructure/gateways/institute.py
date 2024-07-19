from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.institute import (
    InstituteReader,
    InstituteSaver,
)
from pocket_kai.domain.entitites.institute import InstituteEntity
from pocket_kai.infrastructure.database.models.kai import InstituteModel


class InstituteGateway(InstituteReader, InstituteSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def db_to_entity(
        institute_record: InstituteModel | None,
    ) -> InstituteEntity | None:
        if not institute_record:
            return None

        return InstituteEntity(
            id=institute_record.id,
            created_at=institute_record.created_at,
            kai_id=institute_record.kai_id,
            name=institute_record.name,
        )

    async def get_by_kai_id(self, kai_id: int) -> InstituteEntity | None:
        return self.db_to_entity(
            await self._session.scalar(
                select(InstituteModel).where(InstituteModel.kai_id == kai_id),
            ),
        )

    async def get_by_id(self, id: str) -> InstituteEntity | None:
        return self.db_to_entity(
            await self._session.get(InstituteModel, id),
        )

    async def save(self, institute: InstituteEntity) -> None:
        await self._session.execute(
            insert(InstituteModel).values(
                id=institute.id,
                created_at=institute.created_at,
                kai_id=institute.kai_id,
                name=institute.name,
            ),
        )
