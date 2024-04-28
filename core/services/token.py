import uuid
from uuid import UUID

from core.services.base import BaseService
from database.models import Token


class TokenService(BaseService):
    async def create(self, token: UUID = None):
        token = token or uuid.uuid4()

        new_token = Token(token=token)

        self.session.add(new_token)
        await self.session.commit()

        return new_token
