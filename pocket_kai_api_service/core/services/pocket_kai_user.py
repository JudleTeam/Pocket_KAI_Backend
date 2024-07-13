from abc import ABC, abstractmethod

from core.entities.pocket_kai_user import PocketKaiUserEntity
from core.repositories.pocket_kai_user import PocketKaiUserRepositoryBase
from core.security.jwt import JWTManagerProtocol
from core.unit_of_work import UnitOfWorkBase


class PocketKaiUserServiceBase(ABC):
    def __init__(
        self,
        pocket_kai_user_repository: PocketKaiUserRepositoryBase,
        uow: UnitOfWorkBase,
        jwt_manager: JWTManagerProtocol,
    ):
        self.pocket_kai_user_repository = pocket_kai_user_repository
        self.unit_of_work = uow
        self.jwt_manager = jwt_manager

    @abstractmethod
    async def get_by_access_token(self, access_token: str) -> PocketKaiUserEntity:
        raise NotImplementedError


class PocketKaiUserService(PocketKaiUserServiceBase):
    async def get_by_access_token(self, access_token: str) -> PocketKaiUserEntity:
        access_token_payload = self.jwt_manager.decode_access_token(access_token)
        return await self.pocket_kai_user_repository.get_by_id(access_token_payload.sub)
