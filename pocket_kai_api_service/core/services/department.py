from abc import abstractmethod
from typing import Protocol

from api.schemas.department import DepartmentCreate
from core.entities.department import DepartmentEntity
from core.repositories.department import DepartmentRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class DepartmentServiceBase(Protocol):
    def __init__(
        self,
        department_repository: DepartmentRepositoryBase,
        uow: UnitOfWorkBase
    ):
        self.department_repository = department_repository
        self.uow = uow

    @abstractmethod
    async def create(self, department_create: DepartmentCreate) -> DepartmentEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> DepartmentEntity:
        raise NotImplementedError


class DepartmentService(DepartmentServiceBase):
    async def create(self, department_create: DepartmentCreate) -> DepartmentEntity:
        department = await self.department_repository.create(
            kai_id=department_create.kai_id,
            name=department_create.name
        )
        await self.uow.commit()
        return department

    async def get_by_kai_id(self, kai_id: int) -> DepartmentEntity:
        return await self.department_repository.get_by_kai_id(kai_id=kai_id)
