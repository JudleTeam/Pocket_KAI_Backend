from typing import Protocol
from abc import abstractmethod

from pocket_kai.domain.entitites.teacher import TeacherEntity


class TeacherSaver(Protocol):
    @abstractmethod
    async def save(self, teacher: TeacherEntity) -> None:
        """

        :param teacher:
        :return:
        :raise TeacherAlreadyExistsError:
        """
        raise NotImplementedError


class TeacherReader(Protocol):
    @abstractmethod
    async def get_by_id(self, id: str) -> TeacherEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: str) -> TeacherEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def suggest_by_name(self, name: str, limit: int) -> list[TeacherEntity]:
        raise NotImplementedError
