from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.service_token import ServiceTokenReader
from pocket_kai.domain.entitites.service_token import ServiceTokenEntity
from pocket_kai.domain.exceptions.service_token import ServiceTokenNotFoundError
from pocket_kai.infrastructure.database.models import ServiceTokenModel


class ServiceTokenGateway(ServiceTokenReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_token(self, token: str) -> ServiceTokenEntity:
        token_record = await self._session.scalar(
            select(ServiceTokenModel).where(ServiceTokenModel.token == token),
        )

        if token_record is None:
            raise ServiceTokenNotFoundError

        return token_record
