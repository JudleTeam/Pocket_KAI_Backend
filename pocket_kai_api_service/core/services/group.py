from abc import ABC, abstractmethod
from uuid import UUID

from core.entities.group import GroupEntity
from core.repositories.group import GroupRepositoryBase


class GroupServiceBase(ABC):
    def __init__(
        self,
        group_repository: GroupRepositoryBase,
    ):
        self.group_repository = group_repository

    @abstractmethod
    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, group_id: UUID) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, group_name: str) -> GroupEntity:
        raise NotImplementedError


class GroupService(GroupServiceBase):
    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        return await self.group_repository.suggest_by_name(group_name, limit=limit)

    async def get_all(self, limit: int, offset: int) -> list[GroupEntity]:
        return await self.group_repository.list(limit=limit, offset=offset)

    async def get_by_id(self, group_id: UUID) -> GroupEntity:
        return await self.group_repository.get_by_id(group_id)

    async def get_by_name(self, group_name: str) -> GroupEntity:
        return await self.group_repository.get_by_name(group_name)
