from abc import ABC, abstractmethod
from uuid import UUID

from api.schemas.group import GroupCreate, GroupUpdate
from core.entities.group import GroupEntity
from core.repositories.group import GroupRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class GroupServiceBase(ABC):
    def __init__(
        self,
        group_repository: GroupRepositoryBase,
        uow: UnitOfWorkBase,
    ):
        self.group_repository = group_repository
        self.uow = uow

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

    @abstractmethod
    async def create(self, group_create: GroupCreate) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def update(self, group_id: UUID, group_update: GroupUpdate) -> GroupEntity:
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

    async def create(self, group_create: GroupCreate) -> GroupEntity:
        new_group = await self.group_repository.create(
            group_name=group_create.group_name,
            kai_id=group_create.kai_id,
        )
        await self.uow.commit()
        return new_group

    async def update(self, group_id: UUID, group_update: GroupUpdate) -> GroupEntity:
        updated_group = GroupEntity(
            id=group_id,
            kai_id=group_update.kai_id,
            group_leader_id=group_update.group_leader_id,
            pinned_text=group_update.pinned_text,
            group_name=group_update.group_name,
            is_verified=group_update.is_verified,
            verified_at=group_update.verified_at,
            parsed_at=group_update.parsed_at,
            schedule_parsed_at=group_update.schedule_parsed_at,
            syllabus_url=group_update.syllabus_url,
            educational_program_url=group_update.educational_program_url,
            study_schedule_url=group_update.study_schedule_url,
        )
        updated_group = await self.group_repository.update(updated_group)
        await self.uow.commit()
        return updated_group
