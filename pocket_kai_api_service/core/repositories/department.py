from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.department import DepartmentEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import DepartmentModel


class DepartmentRepositoryBase(GenericRepository[DepartmentEntity], ABC):
    entity = DepartmentEntity

    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> DepartmentEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> DepartmentEntity:
        raise NotImplementedError


class SADepartmentRepository(
    GenericSARepository[DepartmentEntity],
    DepartmentRepositoryBase,
):
    model_cls = DepartmentModel

    async def get_by_kai_id(self, kai_id: int) -> DepartmentEntity:
        stmt = select(DepartmentModel).where(DepartmentModel.kai_id == kai_id)
        department = await self._session.scalar(stmt)
        if department is None:
            raise EntityNotFoundError(entity=DepartmentEntity, find_query=kai_id)
        return await self._convert_db_to_entity(department)

    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> DepartmentEntity:
        new_department = DepartmentModel(kai_id=kai_id, name=name)
        await self._add(new_department)
        return await self._convert_db_to_entity(new_department)
