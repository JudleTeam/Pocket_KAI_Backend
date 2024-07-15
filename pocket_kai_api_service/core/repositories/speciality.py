from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.speciality import SpecialityEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import SpecialityModel


class SpecialityRepositoryBase(GenericRepository[SpecialityEntity], ABC):
    entity = SpecialityEntity

    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> SpecialityEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        kai_id: int,
        code: str,
        name: str,
    ) -> SpecialityEntity:
        raise NotImplementedError


class SASpecialityRepository(
    GenericSARepository[SpecialityEntity],
    SpecialityRepositoryBase,
):
    model_cls = SpecialityModel

    async def get_by_kai_id(self, kai_id: int) -> SpecialityEntity:
        stmt = select(SpecialityModel).where(SpecialityModel.kai_id == kai_id)
        speciality = await self._session.scalar(stmt)
        if speciality is None:
            raise EntityNotFoundError(entity=SpecialityEntity, find_query=kai_id)
        return await self._convert_db_to_entity(speciality)

    async def create(
        self,
        kai_id: int,
        code: str,
        name: str,
    ) -> SpecialityEntity:
        new_speciality = SpecialityModel(kai_id=kai_id, name=name, code=code)
        await self._add(new_speciality)
        return await self._convert_db_to_entity(new_speciality)
