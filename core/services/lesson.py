from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from core.entities.lesson import LessonEntity, WeekParity
from core.repositories.lesson import LessonRepositoryBase


class LessonServiceBase(Protocol):
    def __init__(
        self,
        lesson_repository: LessonRepositoryBase
    ):
        self.lesson_repository = lesson_repository

    @abstractmethod
    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        raise NotImplementedError


class LessonService(LessonServiceBase):
    async def get_by_group_id(self, group_id: UUID, week_parity: WeekParity = WeekParity.any) -> list[LessonEntity]:
        return await self.lesson_repository.get_by_group_id(group_id, week_parity=week_parity)
