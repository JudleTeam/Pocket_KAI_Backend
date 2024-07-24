from dataclasses import asdict

from pocket_kai.application.dto.group import (
    GroupExtendedDTO,
    GroupPatchDTO,
    NewGroupDTO,
)
from pocket_kai.application.interfaces.common import DateTimeManager, UUIDGenerator
from pocket_kai.application.interfaces.entities.department import DepartmentReader
from pocket_kai.application.interfaces.entities.group import (
    GroupGatewayProtocol,
    GroupReader,
    GroupSaver,
)
from pocket_kai.application.interfaces.entities.institute import InstituteReader
from pocket_kai.application.interfaces.entities.profile import ProfileReader
from pocket_kai.application.interfaces.entities.speciality import SpecialityReader
from pocket_kai.application.interfaces.unit_of_work import UnitOfWork
from pocket_kai.domain.entitites.group import GroupEntity
from pocket_kai.domain.exceptions.group import GroupNotFoundError


class GroupExtendedDTOConverter:
    def __init__(
        self,
        profile_gateway: ProfileReader,
        speciality_gateway: SpecialityReader,
        department_gateway: DepartmentReader,
        institute_gateway: InstituteReader,
    ):
        self._profile_gateway = profile_gateway
        self._speciality_gateway = speciality_gateway
        self._department_gateway = department_gateway
        self._institute_gateway = institute_gateway

    async def __call__(self, entity: GroupEntity) -> GroupExtendedDTO:
        return GroupExtendedDTO(
            **asdict(entity),
            profile=await self._profile_gateway.get_by_id(entity.profile_id)
            if entity.profile_id
            else None,
            speciality=await self._speciality_gateway.get_by_id(entity.speciality_id)
            if entity.speciality_id
            else None,
            department=await self._department_gateway.get_by_id(entity.department_id)
            if entity.department_id
            else None,
            institute=await self._institute_gateway.get_by_id(entity.institute_id)
            if entity.institute_id
            else None,
        )


class SuggestGroupsByNameInteractor:
    def __init__(self, group_gateway: GroupReader):
        self._group_gateway = group_gateway

    async def __call__(
        self,
        group_name: str,
        limit: int,
        offset: int,
    ) -> list[GroupEntity]:
        return await self._group_gateway.suggest_by_name(
            group_name=group_name,
            limit=limit,
            offset=offset,
        )


class GetAllGroupsInteractor:
    def __init__(
        self,
        group_gateway: GroupReader,
        group_extended_dto_converter: GroupExtendedDTOConverter,
    ):
        self._group_gateway = group_gateway
        self._group_extended_dto_converter = group_extended_dto_converter

    async def __call__(
        self,
        is_short: bool,
        limit: int,
        offset: int,
    ) -> list[GroupExtendedDTO] | list[GroupEntity]:
        if is_short:
            return await self._group_gateway.get_all(limit=limit, offset=offset)
        else:
            return await self._group_gateway.get_all_extended(
                limit=limit,
                offset=offset,
            )


class GetGroupByNameInteractor:
    def __init__(
        self,
        group_gateway: GroupReader,
        group_extended_dto_converter: GroupExtendedDTOConverter,
    ):
        self._group_gateway = group_gateway
        self._group_extended_dto_converter = group_extended_dto_converter

    async def __call__(self, group_name: str) -> GroupEntity:
        return await self._group_extended_dto_converter(
            await self._group_gateway.get_by_name(group_name=group_name),
        )


class GetGroupByIdInteractor:
    def __init__(
        self,
        group_gateway: GroupReader,
        group_extended_dto_converter: GroupExtendedDTOConverter,
    ):
        self._group_gateway = group_gateway
        self._group_extended_dto_converter = group_extended_dto_converter

    async def __call__(self, group_id: str) -> GroupEntity:
        return await self._group_extended_dto_converter(
            await self._group_gateway.get_by_id(id=group_id),
        )


class CreateGroupInteractor:
    def __init__(
        self,
        group_gateway: GroupSaver,
        uuid_generator: UUIDGenerator,
        datetime_manager: DateTimeManager,
        uow: UnitOfWork,
        group_extended_dto_converter: GroupExtendedDTOConverter,
    ):
        self._group_gateway = group_gateway
        self._uuid_generator = uuid_generator
        self._datetime_manager = datetime_manager
        self._uow = uow
        self._group_extended_dto_converter = group_extended_dto_converter

    async def __call__(self, new_group: NewGroupDTO) -> GroupExtendedDTO:
        group = GroupEntity(
            id=self._uuid_generator(),
            created_at=self._datetime_manager.now(),
            kai_id=new_group.kai_id,
            group_leader_id=None,
            pinned_text=None,
            group_name=new_group.group_name,
            is_verified=False,
            verified_at=None,
            parsed_at=None,
            schedule_parsed_at=None,
            syllabus_url=None,
            educational_program_url=None,
            study_schedule_url=None,
            speciality_id=None,
            profile_id=None,
            department_id=None,
            institute_id=None,
        )

        await self._group_gateway.save(group)
        await self._uow.commit()

        return await self._group_extended_dto_converter(group)


class PatchGroupByNameInteractor:
    def __init__(
        self,
        group_gateway: GroupGatewayProtocol,
        uow: UnitOfWork,
        group_extended_dto_converter: GroupExtendedDTOConverter,
    ):
        self._group_gateway = group_gateway
        self._uow = uow
        self._group_extended_dto_converter = group_extended_dto_converter

    async def __call__(
        self,
        group_name: str,
        group_patch: GroupPatchDTO,
    ) -> GroupExtendedDTO:
        await self._group_gateway.patch_by_name(
            group_name=group_name,
            group_patch=group_patch,
        )
        await self._uow.commit()

        group = await self._group_gateway.get_by_name(group_name=group_name)
        if group is None:
            raise GroupNotFoundError

        return await self._group_extended_dto_converter(group)


class PatchGroupByIdInteractor:
    def __init__(
        self,
        group_gateway: GroupGatewayProtocol,
        uow: UnitOfWork,
        group_extended_dto_converter: GroupExtendedDTOConverter,
    ):
        self._group_gateway = group_gateway
        self._uow = uow
        self._group_extended_dto_converter = group_extended_dto_converter

    async def __call__(
        self,
        group_id: str,
        group_patch: GroupPatchDTO,
    ) -> GroupExtendedDTO:
        await self._group_gateway.patch_by_id(
            id=group_id,
            group_patch=group_patch,
        )
        await self._uow.commit()

        group = await self._group_gateway.get_by_id(id=group_id)
        if group is None:
            raise GroupNotFoundError

        return await self._group_extended_dto_converter(group)
