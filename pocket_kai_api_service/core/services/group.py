from datetime import datetime

from abc import ABC, abstractmethod
from uuid import UUID

from api.schemas.group import GroupPatch
from core.entities.group import GroupEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.department import DepartmentRepositoryBase
from core.repositories.group import GroupRepositoryBase
from core.repositories.institute import InstituteRepositoryBase
from core.repositories.profile import ProfileRepositoryBase
from core.repositories.speciality import SpecialityRepositoryBase
from utils.kai_parser_api.schemas import UserAbout


class GroupServiceBase(ABC):
    def __init__(
        self,
        group_repository: GroupRepositoryBase,
        specialty_repository: SpecialityRepositoryBase,
        profile_repository: ProfileRepositoryBase,
        institute_repository: InstituteRepositoryBase,
        department_repository: DepartmentRepositoryBase,
    ):
        self.group_repository = group_repository
        self.specialty_repository = specialty_repository
        self.profile_repository = profile_repository
        self.institute_repository = institute_repository
        self.department_repository = department_repository

    @abstractmethod
    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, group_id: UUID) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, group_name: str) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(self, group_name: str, kai_id: int) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def update(self, group: GroupEntity) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def patch(self, group: GroupEntity, group_patch: GroupPatch) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def add_additional_data_from_user_about(
        self,
        group_name: str,
        user_about: UserAbout,
    ) -> GroupEntity:
        raise NotImplementedError


class GroupService(GroupServiceBase):
    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        return await self.group_repository.suggest_by_name(group_name, limit=limit)

    async def get_all(self, limit: int, offset: int) -> list[GroupEntity]:
        return await self.group_repository.list(limit=limit, offset=offset)

    async def get_by_id(self, group_id: UUID) -> GroupEntity:
        return await self.group_repository.get_by_id(group_id)

    async def get_by_name(self, group_name: str) -> GroupEntity:
        return await self.group_repository.get_by_name(group_name)

    async def create(self, group_name: str, kai_id: int) -> GroupEntity:
        return await self.group_repository.create(
            group_name=group_name,
            kai_id=kai_id,
        )

    async def patch(self, group: GroupEntity, group_patch: GroupPatch) -> GroupEntity:
        for attr, value in group_patch.model_dump(exclude_unset=True).items():
            group.__setattr__(attr, value)
        patched_group = await self.group_repository.update(group)
        return patched_group

    async def update(self, group: GroupEntity) -> GroupEntity:
        return await self.group_repository.update(group)

    async def add_additional_data_from_user_about(
        self,
        group_name: str,
        user_about: UserAbout,
    ) -> GroupEntity:
        group = await self.group_repository.get_by_name(group_name=group_name)

        try:
            speciality = await self.specialty_repository.get_by_kai_id(
                kai_id=user_about.specId,
            )
        except EntityNotFoundError:
            speciality = await self.specialty_repository.create(
                kai_id=user_about.specId,
                code=user_about.specCode,
                name=user_about.specName,
            )

        try:
            profile = await self.profile_repository.get_by_kai_id(
                kai_id=user_about.profileId,
            )
        except EntityNotFoundError:
            profile = await self.profile_repository.create(
                kai_id=user_about.profileId,
                name=user_about.profileName,
            )

        try:
            institute = await self.institute_repository.get_by_kai_id(
                kai_id=user_about.instId,
            )
        except EntityNotFoundError:
            institute = await self.institute_repository.create(
                kai_id=user_about.instId,
                name=user_about.instName,
            )

        try:
            department = await self.department_repository.get_by_kai_id(
                kai_id=user_about.kafId,
            )
        except EntityNotFoundError:
            department = await self.department_repository.create(
                kai_id=user_about.kafId,
                name=user_about.kafName,
            )

        group.institute_id = institute.id
        group.speciality_id = speciality.id
        group.profile_id = profile.id
        group.department_id = department.id
        group.is_verified = True
        group.verified_at = datetime.utcnow()
        group.parsed_at = datetime.utcnow()

        group = await self.group_repository.update(group)

        return group
