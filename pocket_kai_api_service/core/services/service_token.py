from abc import abstractmethod
from typing import Protocol

from core.entities.service_token import ServiceTokenEntity
from core.repositories.service_token import ServiceTokenRepositoryBase


class ServiceTokenServiceBase(Protocol):
    def __init__(
        self,
        service_token_repository: ServiceTokenRepositoryBase
    ):
        self.service_token_repository = service_token_repository

    @abstractmethod
    async def get_by_token(self, token: str) -> ServiceTokenEntity:
        raise NotImplementedError


class ServiceTokenService(ServiceTokenServiceBase):
    async def get_by_token(self, token: str) -> ServiceTokenEntity:
        return await self.service_token_repository.get_by_token(token)

