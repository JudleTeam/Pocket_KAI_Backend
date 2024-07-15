from abc import ABC, abstractmethod

from core.entities.task import TaskEntity
from core.repositories.base import GenericRepository, GenericSARepository
from database.models.task import TaskModel


class TaskRepositoryBase(GenericRepository[TaskEntity], ABC):
    entity = TaskEntity

    @abstractmethod
    async def create(
        self,
        name: str,
        type: str,
        status: str,
        login: str | None,
        group_name: str | None,
        errors: str | None,
    ) -> TaskEntity:
        raise NotImplementedError


class SATaskRepository(GenericSARepository[TaskEntity], TaskRepositoryBase):
    model_cls = TaskModel

    async def create(
        self,
        name: str,
        type: str,
        status: str,
        login: str | None,
        group_name: str | None,
        errors: str | None,
    ) -> TaskEntity:
        new_task = TaskModel(
            name=name,
            type=type,
            login=login,
            group_name=group_name,
            status=status,
            errors=errors,
        )
        await self._add(new_task)
        return await self._convert_db_to_entity(new_task)
