from abc import ABC, abstractmethod

from core.common import TaskStatus, TaskType
from core.entities.task import TaskEntity
from core.repositories.task import TaskRepositoryBase
from core.unit_of_work import UnitOfWorkBase


class TaskServiceBase(ABC):
    def __init__(
        self,
        task_repository: TaskRepositoryBase,
        uow: UnitOfWorkBase,
    ):
        self.task_repository = task_repository
        self.uow = uow

    @abstractmethod
    async def update(self, task: TaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        name: str,
        type: TaskType,
        status: TaskStatus,
        login: str | None = None,
        group_name: str | None = None,
        errors: str | None = None,
    ) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        limit: int,
        offset: int,
        group_name: str | None,
        login: str | None,
        type: TaskType | None,
        status: TaskStatus | None,
    ) -> list[TaskEntity]:
        raise NotImplementedError


class TaskService(TaskServiceBase):
    async def create(
        self,
        name: str,
        type: TaskType,
        status: TaskStatus,
        login: str | None = None,
        group_name: str | None = None,
        errors: str | None = None,
    ) -> TaskEntity:
        new_task = await self.task_repository.create(
            name=name,
            type=type,
            status=status,
            login=login,
            group_name=group_name,
            errors=errors,
        )
        await self.uow.commit()
        return new_task

    async def get(
        self,
        limit: int,
        offset: int,
        group_name: str | None,
        login: str | None,
        type: TaskType | None,
        status: TaskStatus | None,
    ) -> list[TaskEntity]:
        return await self.task_repository.get_tasks_order_by_created_at(
            limit=limit,
            offset=offset,
            group_name=group_name,
            login=login,
            type=type,
            status=status,
        )

    async def update(self, task: TaskEntity) -> TaskEntity:
        task = await self.task_repository.update(task)
        await self.uow.commit()
        return task
