import dataclasses

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.refresh_token import (
    RefreshTokenReader,
    RefreshTokenSaver,
    RefreshTokenUpdater,
)
from pocket_kai.domain.entitites.refresh_token import RefreshTokenEntity
from pocket_kai.infrastructure.database.models import RefreshTokenModel


class RefreshTokenGateway(RefreshTokenReader, RefreshTokenSaver, RefreshTokenUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(
        refresh_token_record: RefreshTokenModel | None,
    ) -> RefreshTokenEntity | None:
        if refresh_token_record is None:
            return None
        return RefreshTokenEntity(
            id=refresh_token_record.id,
            created_at=refresh_token_record.created_at,
            token=refresh_token_record.token,
            name=refresh_token_record.name,
            is_revoked=refresh_token_record.is_revoked,
            issued_at=refresh_token_record.issued_at,
            expires_at=refresh_token_record.expires_at,
            last_used_at=refresh_token_record.last_used_at,
            revoked_at=refresh_token_record.revoked_at,
            user_id=refresh_token_record.user_id,
        )

    async def get_by_token(self, token: str) -> RefreshTokenEntity | None:
        return self._db_to_entity(
            await self._session.scalar(
                select(RefreshTokenModel).where(RefreshTokenModel.token == token),
            ),
        )

    async def get_by_id(self, id: str) -> RefreshTokenEntity | None:
        return self._db_to_entity(
            await self._session.get(RefreshTokenModel, id),
        )

    async def save(self, refresh_token: RefreshTokenEntity) -> None:
        await self._session.execute(
            insert(RefreshTokenModel).values(**dataclasses.asdict(refresh_token)),
        )

    async def update(self, refresh_token: RefreshTokenEntity) -> None:
        update_dict = dataclasses.asdict(refresh_token)
        update_dict.pop('id')

        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == refresh_token.id)
            .values(**update_dict),
        )
