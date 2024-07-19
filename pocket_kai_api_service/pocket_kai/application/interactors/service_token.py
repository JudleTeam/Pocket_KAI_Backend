from pocket_kai.application.interfaces.entities.service_token import ServiceTokenReader
from pocket_kai.domain.exceptions.service_token import ServiceTokenError


class CheckServiceTokenInteractor:
    def __init__(self, service_token_gateway: ServiceTokenReader):
        self._service_token_gateway = service_token_gateway

    async def __call__(self, token: str) -> bool:
        try:
            await self._service_token_gateway.get_by_token(token=token)
        except ServiceTokenError:
            return False

        return True
