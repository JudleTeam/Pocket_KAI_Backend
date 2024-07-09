from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.discipline import DisciplineEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import Discipline


class DisciplineRepositoryBase(GenericRepository[DisciplineEntity], ABC):
    entity = DisciplineEntity

    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> DisciplineEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> DisciplineEntity:
        raise NotImplementedError


class SADisciplineRepository(
    GenericSARepository[DisciplineEntity],
    DisciplineRepositoryBase,
):
    model_cls = Discipline

    async def get_by_kai_id(self, kai_id: int) -> DisciplineEntity:
        stmt = select(Discipline).where(Discipline.kai_id == kai_id)
        discipline = await self._session.scalar(stmt)
        if discipline is None:
            raise EntityNotFoundError(entity=DisciplineEntity, find_query=kai_id)
        return await self._convert_db_to_entity(discipline)

    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> DisciplineEntity:
        new_discipline = Discipline(kai_id=kai_id, name=name)
        await self._add(new_discipline)
        return await self._convert_db_to_entity(new_discipline)
