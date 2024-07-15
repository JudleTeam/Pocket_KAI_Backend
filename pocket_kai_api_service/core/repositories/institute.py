from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.institute import InstituteEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import InstituteModel


class InstituteRepositoryBase(GenericRepository[InstituteEntity], ABC):
    entity = InstituteEntity

    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> InstituteEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> InstituteEntity:
        raise NotImplementedError


class SAInstituteRepository(
    GenericSARepository[InstituteEntity],
    InstituteRepositoryBase,
):
    model_cls = InstituteModel

    async def get_by_kai_id(self, kai_id: int) -> InstituteEntity:
        stmt = select(InstituteModel).where(InstituteModel.kai_id == kai_id)
        institute = await self._session.scalar(stmt)
        if institute is None:
            raise EntityNotFoundError(entity=InstituteEntity, find_query=kai_id)
        return await self._convert_db_to_entity(institute)

    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> InstituteEntity:
        new_institute = InstituteModel(kai_id=kai_id, name=name)
        await self._add(new_institute)
        return await self._convert_db_to_entity(new_institute)
