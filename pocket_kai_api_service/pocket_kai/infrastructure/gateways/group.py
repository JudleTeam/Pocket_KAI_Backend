import dataclasses

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pocket_kai.application.dto.group import GroupExtendedDTO, GroupPatchDTO
from pocket_kai.application.interfaces.entities.group import (
    GroupReader,
    GroupSaver,
    GroupUpdater,
)
from pocket_kai.domain.entitites.group import GroupEntity
from pocket_kai.domain.exceptions.base import BadRelatedEntityError
from pocket_kai.domain.exceptions.group import GroupAlreadyExistsError
from pocket_kai.infrastructure.database.models.kai import GroupModel
from pocket_kai.infrastructure.gateways.department import DepartmentGateway
from pocket_kai.infrastructure.gateways.institute import InstituteGateway
from pocket_kai.infrastructure.gateways.profile import ProfileGateway
from pocket_kai.infrastructure.gateways.speciality import SpecialityGateway


class GroupGateway(GroupReader, GroupSaver, GroupUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _db_to_entity(group_record: GroupModel | None) -> GroupEntity | None:
        if group_record is None:
            return None

        return GroupEntity(
            id=group_record.id,
            created_at=group_record.created_at,
            kai_id=group_record.kai_id,
            group_leader_id=group_record.group_leader_id,
            pinned_text=group_record.pinned_text,
            group_name=group_record.group_name,
            is_verified=group_record.is_verified,
            verified_at=group_record.verified_at,
            parsed_at=group_record.parsed_at,
            schedule_parsed_at=group_record.schedule_parsed_at,
            syllabus_url=group_record.syllabus_url,
            educational_program_url=group_record.educational_program_url,
            study_schedule_url=group_record.study_schedule_url,
            speciality_id=group_record.speciality_id,
            profile_id=group_record.profile_id,
            department_id=group_record.department_id,
            institute_id=group_record.institute_id,
        )

    @staticmethod
    def _db_to_entity_extended(
        group_record: GroupModel | None,
    ) -> GroupExtendedDTO | None:
        if group_record is None:
            return None

        return GroupExtendedDTO(
            id=group_record.id,
            created_at=group_record.created_at,
            kai_id=group_record.kai_id,
            group_leader_id=group_record.group_leader_id,
            pinned_text=group_record.pinned_text,
            group_name=group_record.group_name,
            is_verified=group_record.is_verified,
            verified_at=group_record.verified_at,
            parsed_at=group_record.parsed_at,
            schedule_parsed_at=group_record.schedule_parsed_at,
            syllabus_url=group_record.syllabus_url,
            educational_program_url=group_record.educational_program_url,
            study_schedule_url=group_record.study_schedule_url,
            speciality_id=group_record.speciality_id,
            profile_id=group_record.profile_id,
            department_id=group_record.department_id,
            institute_id=group_record.institute_id,
            profile=ProfileGateway.db_to_entity(group_record.profile),
            speciality=SpecialityGateway.db_to_entity(group_record.speciality),
            department=DepartmentGateway.db_to_entity(group_record.department),
            institute=InstituteGateway.db_to_entity(group_record.institute),
        )

    async def get_by_id(self, id: str) -> GroupEntity | None:
        return self._db_to_entity(
            await self._session.get(GroupModel, id),
        )

    async def suggest_by_name(
        self,
        group_name: str,
        limit: int,
        offset: int,
    ) -> list[GroupEntity]:
        groups = await self._session.scalars(
            select(GroupModel)
            .where(GroupModel.group_name.startswith(group_name))
            .order_by(GroupModel.group_name)
            .limit(limit)
            .offset(offset),
        )

        return [self._db_to_entity(group) for group in groups.all()]

    async def get_all(self, limit: int, offset: int) -> list[GroupEntity]:
        groups = await self._session.scalars(
            select(GroupModel).limit(limit).offset(offset),
        )

        return [self._db_to_entity(group) for group in groups.all()]

    async def get_all_extended(self, limit: int, offset: int) -> list[GroupExtendedDTO]:
        groups = await self._session.scalars(
            select(GroupModel)
            .limit(limit)
            .offset(offset)
            .options(
                selectinload(GroupModel.profile),
                selectinload(GroupModel.speciality),
                selectinload(GroupModel.department),
                selectinload(GroupModel.institute),
            ),
        )

        return [self._db_to_entity_extended(group) for group in groups.all()]

    async def get_by_name(self, group_name: str) -> GroupEntity | None:
        return self._db_to_entity(
            await self._session.scalar(
                select(GroupModel).where(GroupModel.group_name == group_name),
            ),
        )

    async def save(self, group: GroupEntity) -> None:
        try:
            await self._session.execute(
                insert(GroupModel).values(**dataclasses.asdict(group)),
            )
        except IntegrityError:
            raise GroupAlreadyExistsError

    async def update(self, group: GroupEntity) -> None:
        update_dict = dataclasses.asdict(group)
        update_dict.pop('id')

        try:
            await self._session.execute(
                update(GroupModel)
                .where(GroupModel.id == group.id)
                .values(**update_dict),
            )
        except IntegrityError:
            raise BadRelatedEntityError

    async def patch_by_name(self, group_name: str, group_patch: GroupPatchDTO) -> None:
        try:
            await self._session.execute(
                update(GroupModel)
                .where(GroupModel.group_name == group_name)
                .values(**group_patch.model_dump(exclude_unset=True)),
            )
        except IntegrityError:
            raise BadRelatedEntityError

    async def patch_by_id(self, id: str, group_patch: GroupPatchDTO) -> None:
        try:
            await self._session.execute(
                update(GroupModel)
                .where(GroupModel.id == id)
                .values(**group_patch.model_dump(exclude_unset=True)),
            )
        except IntegrityError:
            raise BadRelatedEntityError
