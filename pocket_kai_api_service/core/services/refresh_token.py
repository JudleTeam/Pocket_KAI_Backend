from datetime import datetime

from uuid import UUID, uuid4

from abc import ABC, abstractmethod

from core.entities.refresh_token import RefreshTokenEntity
from core.repositories.refresh_token import RefreshTokenRepositoryBase
from core.security.jwt import JWTManagerProtocol


class RefreshTokenServiceBase(ABC):
    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepositoryBase,
        jwt_manager: JWTManagerProtocol,
    ):
        self.refresh_token_repository = refresh_token_repository
        self.jwt_manager = jwt_manager

    @abstractmethod
    async def issue_new_token(self, user_id: UUID) -> RefreshTokenEntity:
        raise NotImplementedError

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> RefreshTokenEntity:
        raise NotImplementedError


class RefreshTokenService(RefreshTokenServiceBase):
    async def issue_new_token(self, user_id: UUID) -> RefreshTokenEntity:
        refresh_token_id = uuid4()
        refresh_token = self.jwt_manager.create_refresh_token(
            jti=str(refresh_token_id),
            user_id=str(user_id),
        )
        refresh_token_payload = self.jwt_manager.decode_refresh_token(refresh_token)

        refresh_token_entity = await self.refresh_token_repository.create(
            id=refresh_token_id,
            token=refresh_token,
            name=None,
            issued_at=refresh_token_payload.iat,
            expires_at=refresh_token_payload.exp,
            user_id=user_id,
        )

        return refresh_token_entity

    async def refresh_token(self, refresh_token: str) -> RefreshTokenEntity:
        refresh_token_payload = self.jwt_manager.decode_refresh_token(refresh_token)

        refresh_token_from_storage = await self.refresh_token_repository.get_by_id(
            id=refresh_token_payload.jti,
        )

        # Время жизни обновляется
        new_refresh_token = self.jwt_manager.create_refresh_token(
            jti=str(refresh_token_payload.jti),
            user_id=str(refresh_token_payload.sub),
        )

        new_refresh_token_payload = self.jwt_manager.decode_refresh_token(
            token=new_refresh_token,
        )

        refresh_token_from_storage.expires_at = new_refresh_token_payload.exp.replace(
            tzinfo=None,
        )
        refresh_token_from_storage.issued_at = new_refresh_token_payload.iat.replace(
            tzinfo=None,
        )
        refresh_token_from_storage.last_used_at = datetime.utcnow()
        refresh_token_from_storage.token = new_refresh_token
        refresh_token_from_storage = await self.refresh_token_repository.update(
            refresh_token_from_storage,
        )

        return refresh_token_from_storage
