from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select

from core.entities.lesson import LessonEntity, WeekParity
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.kai import GroupLesson


class LessonRepositoryBase(GenericRepository[LessonEntity], ABC):
    entity = LessonEntity

    @abstractmethod
    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        raise NotImplementedError


class SALessonRepository(GenericSARepository[LessonEntity], LessonRepositoryBase):
    model_cls = GroupLesson

    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        stmt = (
            select(GroupLesson)
            .where(
                GroupLesson.group_id == group_id,
                GroupLesson.parsed_parity.in_({week_parity, WeekParity.any})
            )
            .order_by(GroupLesson.number_of_day, GroupLesson.start_time)
        )
        lessons = await self._session.scalars(stmt)
        return [await self._convert_db_to_entity(lesson) for lesson in lessons.all()]
