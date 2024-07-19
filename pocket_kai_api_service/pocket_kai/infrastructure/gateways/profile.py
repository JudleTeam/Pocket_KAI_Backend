from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pocket_kai.application.interfaces.entities.profile import (
    ProfileReader,
    ProfileSaver,
)
from pocket_kai.domain.entitites.profile import ProfileEntity
from pocket_kai.infrastructure.database.models.kai import ProfileModel


class ProfileGateway(ProfileReader, ProfileSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def db_to_entity(profile_record: ProfileModel | None) -> ProfileEntity | None:
        if not profile_record:
            return None

        return ProfileEntity(
            id=profile_record.id,
            created_at=profile_record.created_at,
            kai_id=profile_record.kai_id,
            name=profile_record.name,
        )

    async def get_by_kai_id(self, kai_id: int) -> ProfileEntity | None:
        return self.db_to_entity(
            await self._session.scalar(
                select(ProfileModel).where(ProfileModel.kai_id == kai_id),
            ),
        )

    async def get_by_id(self, id: str) -> ProfileEntity | None:
        return self.db_to_entity(
            await self._session.get(ProfileModel, id),
        )

    async def save(self, profile: ProfileEntity) -> None:
        await self._session.execute(
            insert(ProfileModel).values(
                id=profile.id,
                created_at=profile.created_at,
                kai_id=profile.kai_id,
                name=profile.name,
            ),
        )
