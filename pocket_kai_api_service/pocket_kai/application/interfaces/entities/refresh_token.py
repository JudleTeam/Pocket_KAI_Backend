from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.refresh_token import RefreshTokenEntity


class RefreshTokenReader(Protocol):
    @abstractmethod
    async def get_by_token(self, token: str) -> RefreshTokenEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> RefreshTokenEntity | None:
        raise NotImplementedError


class RefreshTokenSaver(Protocol):
    @abstractmethod
    async def save(self, refresh_token: RefreshTokenEntity) -> None:
        raise NotImplementedError


class RefreshTokenUpdater(Protocol):
    @abstractmethod
    async def update(self, refresh_token: RefreshTokenEntity) -> None:
        raise NotImplementedError


class RefreshTokenGatewayProtocol(
    RefreshTokenReader,
    RefreshTokenSaver,
    RefreshTokenUpdater,
    Protocol,
): ...
