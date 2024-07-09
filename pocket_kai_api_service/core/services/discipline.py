from abc import abstractmethod
from typing import Protocol

from api.schemas.discipline import DisciplineCreate
from core.entities.discipline import DisciplineEntity
from core.repositories.discipline import DisciplineRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class DisciplineServiceBase(Protocol):
    def __init__(
        self,
        discipline_repository: DisciplineRepositoryBase,
        uow: UnitOfWorkBase,
    ):
        self.discipline_repository = discipline_repository
        self.uow = uow

    @abstractmethod
    async def create(self, discipline_create: DisciplineCreate) -> DisciplineEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> DisciplineEntity:
        raise NotImplementedError


class DisciplineService(DisciplineServiceBase):
    async def create(self, discipline_create: DisciplineCreate) -> DisciplineEntity:
        discipline = await self.discipline_repository.create(
            kai_id=discipline_create.kai_id,
            name=discipline_create.name,
        )
        await self.uow.commit()
        return discipline

    async def get_by_kai_id(self, kai_id: int) -> DisciplineEntity:
        return await self.discipline_repository.get_by_kai_id(kai_id=kai_id)
