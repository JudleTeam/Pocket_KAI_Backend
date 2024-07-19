from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.student import StudentEntity


class StudentReader(Protocol):
    @abstractmethod
    async def get_by_email(self, email: str) -> StudentEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> StudentEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_group_id(self, group_id: str) -> list[StudentEntity]:
        raise NotImplementedError


class StudentSaver(Protocol):
    @abstractmethod
    async def save(self, student: StudentEntity) -> None:
        raise NotImplementedError


class StudentUpdater(Protocol):
    @abstractmethod
    async def update(self, student: StudentEntity) -> None:
        raise NotImplementedError


class StudentGatewayProtocol(StudentReader, StudentSaver, StudentUpdater, Protocol): ...
