from api.kai.schemas.group import GroupCreate
from core.services.base import BaseService
from database.models.kai import Group


class GroupService(BaseService):
    async def add_group(self, group: GroupCreate):
        new_group = Group(**group.model_dump())
        self.session.add(new_group)
        await self.session.commit()

    async def add_groups(self, groups: list[GroupCreate]):
        pass
