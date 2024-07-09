from abc import ABC, abstractmethod

from sqlalchemy import select

from core.entities.service_token import ServiceTokenEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.service_token import ServiceToken


class ServiceTokenRepositoryBase(GenericRepository[ServiceTokenEntity], ABC):
    entity = ServiceTokenEntity

    @abstractmethod
    async def get_by_token(self, token: str) -> ServiceTokenEntity:
        raise NotImplementedError


class SAServiceTokenRepository(
    GenericSARepository[ServiceTokenEntity],
    ServiceTokenRepositoryBase,
):
    model_cls = ServiceToken

    async def get_by_token(self, token: str) -> ServiceTokenEntity:
        stmt = select(ServiceToken).where(ServiceToken.token == token)
        token = await self._session.scalar(stmt)
        if token is None:
            raise EntityNotFoundError(entity=self.entity, find_query=token)

        return await self._convert_db_to_entity(token)
