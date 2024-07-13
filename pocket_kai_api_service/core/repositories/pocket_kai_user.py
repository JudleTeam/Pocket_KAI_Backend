from abc import ABC

from core.entities.pocket_kai_user import PocketKaiUserEntity
from core.repositories.base import GenericRepository, GenericSARepository
from database.models import PocketKAIUser


class PocketKaiUserRepositoryBase(GenericRepository[PocketKaiUserEntity], ABC):
    entity = PocketKaiUserEntity

    async def create(
        self,
        telegram_id: int | None,
        phone: str | None,
        is_blocked: bool,
    ) -> PocketKaiUserEntity:
        raise NotImplementedError


class SAPocketKaiUserRepository(
    GenericSARepository[PocketKaiUserEntity],
    PocketKaiUserRepositoryBase,
):
    model_cls = PocketKAIUser

    async def create(
        self,
        telegram_id: int | None,
        phone: str | None,
        is_blocked: bool,
    ) -> PocketKaiUserEntity:
        pocket_kai_user = PocketKAIUser(
            telegram_id=telegram_id,
            phone=phone,
            is_blocked=is_blocked,
        )
        await self._add(pocket_kai_user)

        return await self._convert_db_to_entity(pocket_kai_user)
