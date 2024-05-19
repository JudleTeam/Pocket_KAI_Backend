import datetime
from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select

from core.entities.lesson import LessonEntity
from core.entities.common import ParsedDatesStatus, WeekParity
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import GroupLesson


class LessonRepositoryBase(GenericRepository[LessonEntity], ABC):
    entity = LessonEntity

    @abstractmethod
    async def create(
        self,
        number_of_day: int,
        original_dates: str | None,
        parsed_parity: WeekParity,
        parsed_dates: list[datetime.date] | None,
        parsed_dates_status: ParsedDatesStatus,
        audience_number: str | None,
        building_number: str | None,
        original_lesson_type: str | None,
        parsed_lesson_type: str | None,
        start_time: datetime.time,
        end_time: datetime.time | None,
        discipline_id: UUID,
        teacher_id: UUID,
        department_id: UUID,
        group_id: UUID
    ) -> LessonEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        raise NotImplementedError


class SALessonRepository(GenericSARepository[LessonEntity], LessonRepositoryBase):
    model_cls = GroupLesson

    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        if week_parity == WeekParity.any:
            parities = {WeekParity.any, WeekParity.odd, WeekParity.even}
        else:
            parities = {WeekParity.any, week_parity}

        stmt = (
            select(GroupLesson)
            .where(
                GroupLesson.group_id == group_id,
                GroupLesson.parsed_parity.in_(parities)
            )
            .order_by(GroupLesson.number_of_day, GroupLesson.start_time)
        )
        lessons = await self._session.scalars(stmt)
        return [await self._convert_db_to_entity(lesson) for lesson in lessons.all()]

    async def create(
        self,
        number_of_day: int,
        original_dates: str | None,
        parsed_parity: WeekParity,
        parsed_dates: list[datetime.date] | None,
        parsed_dates_status: ParsedDatesStatus,
        audience_number: str | None,
        building_number: str | None,
        original_lesson_type: str | None,
        parsed_lesson_type: str | None,
        start_time: datetime.time,
        end_time: datetime.time | None,
        discipline_id: UUID,
        teacher_id: UUID,
        department_id: UUID | None,
        group_id: UUID
    ) -> LessonEntity:
        new_lesson = GroupLesson(
            number_of_day=number_of_day,
            original_dates=original_dates,
            parsed_parity=parsed_parity,
            parsed_dates=parsed_dates,
            parsed_dates_status=parsed_dates_status,
            audience_number=audience_number,
            building_number=building_number,
            original_lesson_type=original_lesson_type,
            parsed_lesson_type=parsed_lesson_type,
            start_time=start_time,
            end_time=end_time,
            discipline_id=discipline_id,
            teacher_id=teacher_id,
            department_id=department_id,
            group_id=group_id
        )
        await self._add(new_lesson)
        await self._session.refresh(new_lesson, ['department', 'teacher', 'discipline'])
        return await self._convert_db_to_entity(new_lesson)
