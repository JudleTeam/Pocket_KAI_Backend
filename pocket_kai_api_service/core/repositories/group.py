from uuid import UUID

import datetime

from abc import ABC, abstractmethod

from sqlalchemy import and_, or_, select

from core.entities.common import WeekParity
from core.entities.group import GroupEntity
from core.exceptions.base import EntityNotFoundError
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import Group, GroupLesson


class GroupRepositoryBase(GenericRepository[GroupEntity], ABC):
    entity = GroupEntity

    @abstractmethod
    async def create(self, group_name: str, kai_id: int) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, group_name: str) -> GroupEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_lesson_data(
        self,
        date: datetime.date | None,
        discipline_id: UUID,
        number_of_day: int,
        parsed_parity: WeekParity,
        original_lesson_type: str | None,
        building_number: str | None,
        audience_number: str | None,
        start_time: datetime.time
    ) -> list[GroupEntity]:
        raise NotImplementedError


class SAGroupRepository(GenericSARepository[GroupEntity], GroupRepositoryBase):
    model_cls = Group

    async def suggest_by_name(self, group_name: str, limit: int) -> list[GroupEntity]:
        stmt = select(Group).where(Group.group_name.startswith(group_name)).limit(limit)
        groups = await self._session.scalars(stmt)
        groups = groups.all()
        return [await self._convert_db_to_entity(group) for group in groups]

    async def get_by_name(self, group_name: str) -> GroupEntity:
        stmt = select(Group).where(Group.group_name == group_name).limit(1)
        group = await self._session.scalar(stmt)
        if group is None:
            raise EntityNotFoundError(entity=GroupEntity, find_query=group_name)
        return await self._convert_db_to_entity(group)

    async def create(self, group_name: str, kai_id: int) -> GroupEntity:
        new_group = Group(group_name=group_name, kai_id=kai_id)
        await self._add(new_group)
        return await self._convert_db_to_entity(new_group)

    async def get_by_lesson_data(
        self,
        date: datetime.date | None,
        discipline_id: UUID,
        number_of_day: int,
        parsed_parity: WeekParity,
        original_lesson_type: str | None,
        building_number: str | None,
        audience_number: str | None,
        start_time: datetime.time
    ) -> list[GroupEntity]:
        stmt = (
            select(Group)
            .join(GroupLesson)
            .where(
                GroupLesson.start_time == start_time,
                GroupLesson.number_of_day == number_of_day,
                GroupLesson.building_number == building_number,
                GroupLesson.audience_number == audience_number,
                GroupLesson.original_lesson_type == original_lesson_type,
                GroupLesson.discipline_id == discipline_id
            )
        )
        # TODO: нужно подумать как это оптимизировать, замедляет запросы с расписанием примерно в 8 раз
        # TODO: возможно будут проблемы, если номер здания и аудитории None

        if date:
            stmt = stmt.where(
                or_(
                    and_(
                        GroupLesson.parsed_dates.is_not(None),
                        GroupLesson.parsed_dates.contains(date)
                    ),
                    and_(
                        GroupLesson.parsed_dates.is_(None),
                        GroupLesson.parsed_parity.in_({WeekParity.any, parsed_parity})
                    )
                )
            )
        else:
            stmt = stmt.where(GroupLesson.parsed_parity.in_({WeekParity.any, parsed_parity}))

        groups = await self._session.scalars(stmt)
        return [await self._convert_db_to_entity(group) for group in groups.all()]
