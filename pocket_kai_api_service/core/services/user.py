from uuid import UUID

from abc import ABC, abstractmethod

from core.entities.user import UserEntity
from core.repositories.user import UserRepositoryBase
from core.security.jwt import JWTManagerProtocol
from core.unit_of_work import UnitOfWorkBase


class UserServiceBase(ABC):
    def __init__(
        self,
        user_repository: UserRepositoryBase,
        uow: UnitOfWorkBase,
        jwt_manager: JWTManagerProtocol,
    ):
        self.user_repository = user_repository
        self.unit_of_work = uow
        self.jwt_manager = jwt_manager

    @abstractmethod
    async def get_by_access_token(self, access_token: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        telegram_id: int | None = None,
        phone: str | None = None,
        is_blocked: bool = False,
    ) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserEntity:
        raise NotImplementedError


class UserService(UserServiceBase):
    async def get_by_access_token(self, access_token: str) -> UserEntity:
        access_token_payload = self.jwt_manager.decode_access_token(access_token)
        return await self.user_repository.get_by_id(access_token_payload.sub)

    async def create(
        self,
        telegram_id: int | None = None,
        phone: str | None = None,
        is_blocked: bool = False,
    ) -> UserEntity:
        return await self.user_repository.create(
            telegram_id=telegram_id,
            phone=phone,
            is_blocked=is_blocked,
        )

    async def get_by_id(self, user_id: UUID) -> UserEntity:
        return await self.user_repository.get_by_id(user_id)
