from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.group import GroupEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import GroupModel


class GroupRepositoryBase(GenericRepository[GroupEntity], ABC):
    entity = GroupEntity

    @abstractmethod
    async def create(self, group_name: str, kai_id: int) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, group_name: str) -> GroupEntity:
        raise NotImplementedError


class SAGroupRepository(GenericSARepository[GroupEntity], GroupRepositoryBase):
    model_cls = GroupModel

    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        stmt = (
            select(GroupModel)
            .where(GroupModel.group_name.startswith(group_name))
            .limit(limit)
        )
        groups = await self._session.scalars(stmt)
        groups = groups.all()
        return [await self._convert_db_to_entity(group) for group in groups]

    async def get_by_name(self, group_name: str) -> GroupEntity:
        stmt = select(GroupModel).where(GroupModel.group_name == group_name).limit(1)
        group = await self._session.scalar(stmt)
        if group is None:
            raise EntityNotFoundError(entity=GroupEntity, find_query=group_name)
        return await self._convert_db_to_entity(group)

    async def create(self, group_name: str, kai_id: int) -> GroupEntity:
        new_group = GroupModel(group_name=group_name, kai_id=kai_id)
        await self._add(new_group)
        return await self._convert_db_to_entity(new_group)
