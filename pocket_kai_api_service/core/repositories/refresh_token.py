from abc import ABC
from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from core.entities.refresh_token import RefreshTokenEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models import RefreshTokenModel


class RefreshTokenRepositoryBase(GenericRepository[RefreshTokenEntity], ABC):
    entity = RefreshTokenEntity

    async def create(
        self,
        id: UUID | str,
        token: str,
        name: str | None,
        issued_at: datetime,
        expires_at: datetime,
        user_id: UUID,
    ) -> RefreshTokenEntity:
        raise NotImplementedError

    async def get_by_token(self, token: str) -> RefreshTokenEntity:
        raise NotImplementedError


class SARefreshTokenRepository(
    GenericSARepository[RefreshTokenEntity],
    RefreshTokenRepositoryBase,
):
    model_cls = RefreshTokenModel

    async def create(
        self,
        id: UUID | str,
        token: str,
        name: str | None,
        issued_at: datetime,
        expires_at: datetime,
        user_id: UUID,
    ) -> RefreshTokenEntity:
        refresh_token = RefreshTokenModel(
            id=id,
            token=token,
            name=name,
            issued_at=issued_at.replace(tzinfo=None),
            expires_at=expires_at.replace(tzinfo=None),
            user_id=user_id,
        )

        await self._add(refresh_token)

        return await self._convert_db_to_entity(refresh_token)

    async def get_by_token(self, token: str) -> RefreshTokenEntity:
        record = await self.session.scalar(
            select(RefreshTokenModel).where(RefreshTokenModel.token == token),
        )

        if record is None:
            raise EntityNotFoundError(entity=self.entity, find_query=token)

        return await self._convert_db_to_entity(record)
