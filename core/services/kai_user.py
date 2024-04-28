from sqlalchemy import select

from core.services.base import BaseService
from database.models.kai import KAIUser


class KaiUserService(BaseService):
    async def get_by_login(self, login: str) -> KAIUser | None:
        stmt = select(KAIUser).where(KAIUser.login == login)

        return await self.session.scalar(stmt)
