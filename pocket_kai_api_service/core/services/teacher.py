from abc import abstractmethod
from typing import Protocol

from api.schemas.teacher import TeacherCreate
from core.entities.teacher import TeacherEntity
from core.repositories.teacher import TeacherRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class TeacherServiceBase(Protocol):
    def __init__(
        self,
        teacher_repository: TeacherRepositoryBase,
        uow: UnitOfWorkBase,
    ):
        self.teacher_repository = teacher_repository
        self.uow = uow

    @abstractmethod
    async def create(self, teacher_create: TeacherCreate) -> TeacherEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: str) -> TeacherEntity:
        raise NotImplementedError


class TeacherService(TeacherServiceBase):
    async def create(self, teacher_create: TeacherCreate) -> TeacherEntity:
        new_teacher = await self.teacher_repository.create(
            login=teacher_create.login,
            name=teacher_create.name,
            department_id=teacher_create.department_id,
        )
        await self.uow.commit()
        return new_teacher

    async def get_by_login(self, login: str) -> TeacherEntity:
        return await self.teacher_repository.get_by_login(login=login)
