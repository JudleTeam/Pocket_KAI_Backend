from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.department import DepartmentEntity


class DepartmentReader(Protocol):
    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> DepartmentEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> DepartmentEntity | None:
        raise NotImplementedError


class DepartmentSaver(Protocol):
    @abstractmethod
    async def save(self, department: DepartmentEntity) -> None:
        raise NotImplementedError


class DepartmentGatewayProtocol(DepartmentReader, DepartmentSaver, Protocol): ...
