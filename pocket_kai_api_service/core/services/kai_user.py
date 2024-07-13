from uuid import UUID

from abc import ABC, abstractmethod

from core.entities.kai_user import KaiUserEntity
from core.repositories.kai_user import KaiUserRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class KaiUserServiceBase(ABC):
    def __init__(
        self,
        kai_user_repository: KaiUserRepositoryBase,
        uow: UnitOfWorkBase,
    ):
        self.uow = uow
        self.kai_user_repository = kai_user_repository

    @abstractmethod
    async def get_by_pocket_kai_user_id(
        self,
        pocket_kai_user_id: UUID,
    ) -> KaiUserEntity:
        raise NotImplementedError


class KaiUserService(KaiUserServiceBase):
    async def get_by_pocket_kai_user_id(
        self,
        pocket_kai_user_id: UUID,
    ) -> KaiUserEntity:
        return await self.kai_user_repository.get_by_pocket_kai_user_id(
            pocket_kai_user_id,
        )
