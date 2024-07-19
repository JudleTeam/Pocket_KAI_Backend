from pocket_kai.application.interfaces.common import DateTimeManager
from pocket_kai.application.interfaces.entities.refresh_token import (
    RefreshTokenGatewayProtocol,
)
from pocket_kai.application.interfaces.jwt import JWTManagerProtocol
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.entitites.refresh_token import RefreshTokenEntity


class RefreshTokenPairInteractor:
    def __init__(
        self,
        refresh_token_reader: RefreshTokenGatewayProtocol,
        datetime_manager: DateTimeManager,
        jwt_manager: JWTManagerProtocol,
        uow: UnitOfWork,
    ):
        self._refresh_token_gateway = refresh_token_reader

        self._datetime_manager = datetime_manager
        self._jwt_manager = jwt_manager

        self._uow = uow

    async def _refresh_token(self, refresh_token: str) -> RefreshTokenEntity:
        refresh_token_payload = self._jwt_manager.decode_refresh_token(refresh_token)

        refresh_token_from_storage = await self._refresh_token_gateway.get_by_id(
            id=refresh_token_payload.jti,
        )

        # Время жизни обновляется
        new_refresh_token = self._jwt_manager.create_refresh_token(
            jti=str(refresh_token_payload.jti),
            user_id=str(refresh_token_payload.sub),
        )

        new_refresh_token_payload = self._jwt_manager.decode_refresh_token(
            token=new_refresh_token,
        )

        refresh_token_from_storage.expires_at = new_refresh_token_payload.exp.replace(
            tzinfo=None,
        )
        refresh_token_from_storage.issued_at = new_refresh_token_payload.iat.replace(
            tzinfo=None,
        )
        refresh_token_from_storage.last_used_at = self._datetime_manager.now()
        refresh_token_from_storage.token = new_refresh_token

        await self._refresh_token_gateway.update(refresh_token_from_storage)

        return refresh_token_from_storage

    async def __call__(self, refresh_token: str) -> tuple[str, str]:
        refresh_token = await self._refresh_token(refresh_token=refresh_token)

        new_access_token = self._jwt_manager.create_access_token(
            user_id=str(refresh_token.user_id),
        )

        await self._uow.commit()

        return new_access_token, refresh_token.token
