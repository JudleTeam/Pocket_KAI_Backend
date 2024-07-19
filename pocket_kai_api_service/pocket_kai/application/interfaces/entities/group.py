from abc import abstractmethod

from typing import Protocol

from pocket_kai.application.dto.group import GroupExtendedDTO, GroupPatchDTO
from pocket_kai.domain.entitites.group import GroupEntity


class GroupReader(Protocol):
    @abstractmethod
    async def get_by_name(self, group_name: str) -> GroupEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> GroupEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def suggest_by_name(
        self,
        group_name: str,
        limit: int,
        offset: int,
    ) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_extended(self, limit: int, offset: int) -> list[GroupExtendedDTO]:
        raise NotImplementedError


class GroupSaver(Protocol):
    @abstractmethod
    async def save(self, group: GroupEntity) -> None:
        raise NotImplementedError


class GroupUpdater(Protocol):
    @abstractmethod
    async def update(self, group: GroupEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def patch_by_name(self, group_name: str, group_patch: GroupPatchDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def patch_by_id(self, id: str, group_patch: GroupPatchDTO) -> None:
        raise NotImplementedError


class GroupGatewayProtocol(GroupReader, GroupSaver, GroupUpdater, Protocol): ...
