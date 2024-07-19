from abc import abstractmethod

from typing import Protocol

from pocket_kai.application.dto.lesson import LessonExtendedDTO, LessonPatchDTO
from pocket_kai.domain.common import WeekParity
from pocket_kai.domain.entitites.lesson import LessonEntity


class LessonReader(Protocol):
    @abstractmethod
    async def get_by_group_id(
        self,
        group_id: str,
        week_parity: WeekParity,
    ) -> list[LessonEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_extended(self, lesson_id: str) -> LessonExtendedDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_group_id_extended(
        self,
        group_id: str,
        week_parity: WeekParity,
    ) -> list[LessonExtendedDTO]:
        raise NotImplementedError


class LessonSaver(Protocol):
    @abstractmethod
    async def save(self, lesson: LessonEntity) -> None:
        raise NotImplementedError


class LessonUpdater(Protocol):
    @abstractmethod
    async def update(self, lesson: LessonEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def patch(self, lesson_id: str, lesson_patch: LessonPatchDTO) -> None:
        raise NotImplementedError


class LessonDeleter(Protocol):
    @abstractmethod
    async def delete(self, lesson_id: str) -> None:
        raise NotImplementedError


class LessonGatewayProtocol(
    LessonReader,
    LessonSaver,
    LessonUpdater,
    LessonDeleter,
    Protocol,
): ...
