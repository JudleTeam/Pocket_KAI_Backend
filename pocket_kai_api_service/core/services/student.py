from uuid import UUID

from abc import ABC, abstractmethod

from core.entities.student import StudentEntity
from core.repositories.student import StudentRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class StudentServiceBase(ABC):
    def __init__(
        self,
        student_repository: StudentRepositoryBase,
        uow: UnitOfWorkBase,
    ):
        self.uow = uow
        self.student_repository = student_repository

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> StudentEntity:
        raise NotImplementedError


class StudentService(StudentServiceBase):
    async def get_by_user_id(self, user_id: UUID) -> StudentEntity:
        return await self.student_repository.get_by_user_id(user_id)
