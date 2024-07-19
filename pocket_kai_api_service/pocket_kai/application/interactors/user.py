from pocket_kai.application.interfaces.jwt import JWTManagerProtocol
from pocket_kai.application.interfaces.entities.user import UserReader


class GetUserByAccessTokenInteractor:
    def __init__(
        self,
        user_gateway: UserReader,
        jwt_manager: JWTManagerProtocol,
    ):
        self._user_gateway = user_gateway
        self._jwt_manager = jwt_manager

    async def __call__(self, access_token: str):
        access_token_payload = self._jwt_manager.decode_access_token(access_token)
        return await self._user_gateway.get_by_id(id=str(access_token_payload.sub))
