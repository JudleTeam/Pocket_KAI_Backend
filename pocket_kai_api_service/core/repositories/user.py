from abc import ABC

from core.entities.user import UserEntity
from core.repositories.base import GenericRepository, GenericSARepository
from database.models import UserModel


class UserRepositoryBase(GenericRepository[UserEntity], ABC):
    entity = UserEntity

    async def create(
        self,
        telegram_id: int | None,
        phone: str | None,
        is_blocked: bool,
    ) -> UserEntity:
        raise NotImplementedError


class SAUserRepository(
    GenericSARepository[UserEntity],
    UserRepositoryBase,
):
    model_cls = UserModel

    async def create(
        self,
        telegram_id: int | None,
        phone: str | None,
        is_blocked: bool,
    ) -> UserEntity:
        user = UserModel(
            telegram_id=telegram_id,
            phone=phone,
            is_blocked=is_blocked,
        )
        await self._add(user)

        return await self._convert_db_to_entity(user)
