from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.profile import ProfileEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import ProfileModel


class ProfileRepositoryBase(GenericRepository[ProfileEntity], ABC):
    entity = ProfileEntity

    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> ProfileEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> ProfileEntity:
        raise NotImplementedError


class SAProfileRepository(
    GenericSARepository[ProfileEntity],
    ProfileRepositoryBase,
):
    model_cls = ProfileModel

    async def get_by_kai_id(self, kai_id: int) -> ProfileEntity:
        stmt = select(ProfileModel).where(ProfileModel.kai_id == kai_id)
        profile = await self._session.scalar(stmt)
        if profile is None:
            raise EntityNotFoundError(entity=ProfileEntity, find_query=kai_id)
        return await self._convert_db_to_entity(profile)

    async def create(
        self,
        kai_id: int,
        name: str,
    ) -> ProfileEntity:
        new_profile = ProfileModel(kai_id=kai_id, name=name)
        await self._add(new_profile)
        return await self._convert_db_to_entity(new_profile)
