from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.discipline import (
    DisciplineReader,
    DisciplineSaver,
)
from pocket_kai.domain.entitites.discipline import DisciplineEntity
from pocket_kai.infrastructure.database.models.kai import DisciplineModel


class DisciplineGateway(DisciplineReader, DisciplineSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(
        discipline_record: DisciplineModel | None,
    ) -> DisciplineEntity | None:
        if not discipline_record:
            return None

        return DisciplineEntity(
            id=discipline_record.id,
            created_at=discipline_record.created_at,
            kai_id=discipline_record.kai_id,
            name=discipline_record.name,
        )

    async def get_by_kai_id(self, kai_id: int) -> DisciplineEntity | None:
        return self._db_to_entity(
            await self._session.scalar(
                select(DisciplineModel).where(DisciplineModel.kai_id == kai_id),
            ),
        )

    async def get_by_id(self, id: str) -> DisciplineEntity | None:
        return self._db_to_entity(
            await self._session.get(DisciplineModel, id),
        )

    async def save(self, discipline: DisciplineEntity) -> None:
        await self._session.execute(
            insert(DisciplineModel).values(
                id=discipline.id,
                created_at=discipline.created_at,
                kai_id=discipline.kai_id,
                name=discipline.name,
            ),
        )
