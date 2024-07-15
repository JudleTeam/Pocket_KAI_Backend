from uuid import UUID

from api.schemas.group import FullGroupRead, GroupCreate, GroupPatch, ShortGroupRead
from core.services.group import GroupServiceBase
from core.unit_of_work import UnitOfWorkBase


class GroupUseCase:
    def __init__(
        self,
        group_service: GroupServiceBase,
        uow: UnitOfWorkBase,
    ):
        self.group_service = group_service
        self.uow = uow

    async def get_all(
        self,
        limit: int,
        offset: int,
        is_short: bool,
    ) -> list[FullGroupRead] | list[ShortGroupRead]:
        groups = await self.group_service.get_all(limit=limit, offset=offset)
        if is_short:
            return [ShortGroupRead.model_validate(group) for group in groups]
        else:
            return [FullGroupRead.model_validate(group) for group in groups]

    async def get_by_name(self, group_name: str) -> FullGroupRead:
        return FullGroupRead.model_validate(
            await self.group_service.get_by_name(group_name),
        )

    async def get_by_id(self, group_id: UUID) -> FullGroupRead:
        return FullGroupRead.model_validate(
            await self.group_service.get_by_id(group_id),
        )

    async def suggest_by_name(
        self,
        group_name: str,
        limit: int,
    ) -> list[ShortGroupRead]:
        groups = await self.group_service.suggest_by_name(
            group_name=group_name,
            limit=limit,
        )
        return [ShortGroupRead.model_validate(group) for group in groups]

    async def create(self, group_create: GroupCreate) -> FullGroupRead:
        group = await self.group_service.create(
            group_name=group_create.group_name,
            kai_id=group_create.kai_id,
        )
        await self.uow.commit()
        return FullGroupRead.model_validate(group)

    async def patch_by_id(
        self,
        group_id: UUID,
        group_patch: GroupPatch,
    ) -> FullGroupRead:
        patched_group = await self.group_service.patch(
            group=await self.group_service.get_by_id(group_id),
            group_patch=group_patch,
        )
        await self.uow.commit()
        return FullGroupRead.model_validate(patched_group)

    async def patch_by_group_name(
        self,
        group_name: str,
        group_patch: GroupPatch,
    ) -> FullGroupRead:
        patched_group = await self.group_service.patch(
            group=await self.group_service.get_by_name(group_name),
            group_patch=group_patch,
        )
        await self.uow.commit()
        return FullGroupRead.model_validate(patched_group)
