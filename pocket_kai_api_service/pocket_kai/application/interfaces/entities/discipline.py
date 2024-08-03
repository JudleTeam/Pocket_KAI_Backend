from abc import abstractmethod

from typing import Protocol

from pocket_kai.application.dto.discipline import DisciplineWithTypesDTO
from pocket_kai.domain.entitites.discipline import DisciplineEntity


class DisciplineReader(Protocol):
    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> DisciplineEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> DisciplineEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_group_id_with_teachers(
        self,
        group_id: str,
    ) -> list[DisciplineWithTypesDTO]:
        raise NotImplementedError


class DisciplineSaver(Protocol):
    @abstractmethod
    async def save(self, discipline: DisciplineEntity) -> None:
        raise NotImplementedError


class DisciplineGatewayProtocol(DisciplineReader, DisciplineSaver, Protocol): ...
