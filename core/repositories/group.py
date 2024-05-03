from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.group import GroupEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import Group


class GroupRepositoryBase(GenericRepository[GroupEntity], ABC):
    entity = GroupEntity

    @abstractmethod
    async def suggest_by_name(self, name: str, limit: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> GroupEntity:
        raise NotImplementedError


class SAGroupRepository(GenericSARepository[GroupEntity], GroupRepositoryBase):
    model_cls = Group

    async def suggest_by_name(self, name: str, limit: int) -> list[GroupEntity]:
        stmt = select(Group).where(Group.group_name.startswith(name)).limit(limit)
        groups = await self._session.scalars(stmt)
        groups = groups.all()
        return [await self._convert_db_to_entity(group) for group in groups]

    async def get_by_name(self, name: str) -> GroupEntity:
        stmt = select(Group).where(Group.group_name == name).limit(1)
        group = await self._session.scalar(stmt)
        if group is None:
            raise EntityNotFoundError(entity=GroupEntity, find_query=name)
        return await self._convert_db_to_entity(group)
