from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.profile import ProfileEntity


class ProfileReader(Protocol):
    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> ProfileEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> ProfileEntity:
        raise NotImplementedError


class ProfileSaver(Protocol):
    @abstractmethod
    async def save(self, profile: ProfileEntity) -> None:
        raise NotImplementedError


class ProfileGatewayProtocol(ProfileReader, ProfileSaver, Protocol): ...
