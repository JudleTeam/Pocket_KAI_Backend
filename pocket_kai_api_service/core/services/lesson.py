import datetime
from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from api.schemas.lesson import LessonCreate, LessonUpdate
from core.entities.lesson import LessonEntity
from core.entities.common import ParsedDatesStatus, WeekParity
from core.repositories.lesson import LessonRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class LessonServiceBase(Protocol):
    def __init__(
        self,
        lesson_repository: LessonRepositoryBase,
        uow: UnitOfWorkBase
    ):
        self.lesson_repository = lesson_repository
        self.uow = uow

    @abstractmethod
    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, lesson_create: LessonCreate) -> LessonEntity:
        raise NotImplementedError

    @abstractmethod
    async def update(self, lesson_id: UUID, lesson_update: LessonUpdate) -> LessonEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, lesson_id: UUID) -> None:
        raise NotImplementedError


class LessonService(LessonServiceBase):
    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        return await self.lesson_repository.get_by_group_id(group_id, week_parity=week_parity)

    async def create(self, lesson_create: LessonCreate) -> LessonEntity:
        lesson = await self.lesson_repository.create(
            number_of_day=lesson_create.number_of_day,
            original_dates=lesson_create.original_dates,
            parsed_parity=lesson_create.parsed_parity,
            parsed_dates=lesson_create.parsed_dates,
            parsed_dates_status=lesson_create.parsed_dates_status,
            audience_number=lesson_create.audience_number,
            building_number=lesson_create.building_number,
            original_lesson_type=lesson_create.original_lesson_type,
            parsed_lesson_type=lesson_create.parsed_lesson_type,
            start_time=lesson_create.start_time,
            end_time=lesson_create.end_time,
            discipline_id=lesson_create.discipline_id,
            teacher_id=lesson_create.teacher_id,
            department_id=lesson_create.department_id,
            group_id=lesson_create.group_id
        )
        await self.uow.commit()
        return lesson

    async def update(self, lesson_id: UUID, lesson_update: LessonUpdate) -> LessonEntity:
        lesson_entity = LessonEntity(
            id=lesson_id,
            number_of_day=lesson_update.number_of_day,
            original_dates=lesson_update.original_dates,
            parsed_parity=lesson_update.parsed_parity,
            parsed_dates=lesson_update.parsed_dates,
            parsed_dates_status=lesson_update.parsed_dates_status,
            start_time=lesson_update.start_time,
            end_time=lesson_update.end_time,
            audience_number=lesson_update.audience_number,
            building_number=lesson_update.building_number,
            original_lesson_type=lesson_update.original_lesson_type,
            parsed_lesson_type=lesson_update.parsed_lesson_type,
            group_id=lesson_update.group_id,
            discipline_id=lesson_update.discipline_id,
            teacher_id=lesson_update.teacher_id,
        )
        updated_lesson = await self.lesson_repository.update(lesson_entity)
        await self.uow.commit()
        return updated_lesson

    async def delete(self, lesson_id: UUID) -> None:
        await self.lesson_repository.delete(lesson_id)
        await self.uow.commit()
