from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.user import UserReader, UserSaver
from pocket_kai.domain.entitites.user import UserEntity
from pocket_kai.infrastructure.database.models import UserModel


class UserGateway(UserReader, UserSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(user_record: UserModel | None) -> UserEntity | None:
        if user_record is None:
            return None

        return UserEntity(
            id=user_record.id,
            created_at=user_record.created_at,
            telegram_id=user_record.telegram_id,
            phone=user_record.phone,
            is_blocked=user_record.is_blocked,
        )

    async def get_by_id(self, id: str) -> UserEntity | None:
        return self._db_to_entity(
            await self._session.get(UserModel, id),
        )

    async def save(self, user: UserEntity) -> None:
        await self._session.execute(
            insert(UserModel).values(
                id=user.id,
                created_at=user.created_at,
                telegram_id=user.telegram_id,
                phone=user.phone,
                is_blocked=user.is_blocked,
            ),
        )
