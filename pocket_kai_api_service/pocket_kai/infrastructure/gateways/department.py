from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.department import (
    DepartmentReader,
    DepartmentSaver,
)
from pocket_kai.domain.entitites.department import DepartmentEntity
from pocket_kai.infrastructure.database.models.kai import DepartmentModel


class DepartmentGateway(DepartmentReader, DepartmentSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def db_to_entity(
        department_record: DepartmentModel | None,
    ) -> DepartmentEntity | None:
        if not department_record:
            return None

        return DepartmentEntity(
            id=department_record.id,
            created_at=department_record.created_at,
            kai_id=department_record.kai_id,
            name=department_record.name,
        )

    async def get_by_kai_id(self, kai_id: int) -> DepartmentEntity | None:
        return self.db_to_entity(
            await self._session.scalar(
                select(DepartmentModel).where(DepartmentModel.kai_id == kai_id),
            ),
        )

    async def get_by_id(self, id: str) -> DepartmentEntity | None:
        return self.db_to_entity(
            await self._session.get(DepartmentModel, id),
        )

    async def save(self, department: DepartmentEntity) -> None:
        await self._session.execute(
            insert(DepartmentModel).values(
                id=department.id,
                created_at=department.created_at,
                kai_id=department.kai_id,
                name=department.name,
            ),
        )
