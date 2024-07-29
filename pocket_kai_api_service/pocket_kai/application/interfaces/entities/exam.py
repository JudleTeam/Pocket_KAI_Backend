from abc import abstractmethod

from typing import Protocol

from pocket_kai.application.dto.exam import ExamExtendedDTO
from pocket_kai.domain.entitites.exam import ExamEntity


class ExamReader(Protocol):
    @abstractmethod
    async def get_by_id(self, exam_id: str) -> ExamEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_extended(self, exam_id: str) -> ExamExtendedDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_group_id(
        self,
        group_id: str,
        academic_year: str | None,
        academic_year_half: int | None,
    ) -> list[ExamEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_group_id_extended(
        self,
        group_id: str,
        academic_year: str | None,
        academic_year_half: int | None,
    ) -> list[ExamExtendedDTO]:
        raise NotImplementedError


class ExamSaver(Protocol):
    @abstractmethod
    async def save(self, exam: ExamEntity) -> None:
        raise NotImplementedError


class ExamUpdater(Protocol):
    @abstractmethod
    async def update(self, exam: ExamEntity) -> None:
        raise NotImplementedError


class ExamDeleter(Protocol):
    @abstractmethod
    async def delete(self, exam_id: str) -> None:
        raise NotImplementedError


class ExamGatewayProtocol(
    ExamReader,
    ExamSaver,
    ExamUpdater,
    ExamDeleter,
    Protocol,
): ...
