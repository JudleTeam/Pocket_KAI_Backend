from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.user import UserEntity


class UserReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: str) -> UserEntity | None:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: UserEntity) -> None:
        raise NotImplementedError
