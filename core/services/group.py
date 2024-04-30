from typing import Sequence
from uuid import UUID

from core.services.base import BaseService
from database.models.kai import Group

from sqlalchemy import select


class GroupNotFoundError(Exception):
    pass


class GroupService(BaseService):
    async def suggest_by_name(self, group_name: str, limit: int) -> Sequence[Group]:
        stmt = select(Group).where(Group.group_name.startswith(group_name)).limit(limit)
        records = await self.session.scalars(stmt)
        return records.all()

    async def get_all(self, limit: int, offset: int) -> Sequence[Group]:
        stmt = select(Group).offset(offset).limit(limit)
        records = await self.session.scalars(stmt)
        return records.all()

    async def get_by_id(self, group_id: UUID) -> Group:
        group = await self.session.get(Group, group_id)
        if group is None:
            raise GroupNotFoundError

        return group

    async def get_by_name(self, group_name: str) -> Group:
        stmt = select(Group).where(Group.group_name == group_name)
        group = await self.session.scalar(stmt)
        if group is None:
            raise GroupNotFoundError

        return group
