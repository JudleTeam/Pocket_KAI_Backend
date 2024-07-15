from abc import ABC, abstractmethod

from sqlalchemy import select

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

    async def get_tasks_order_by_created_at(
        self,
        limit: int,
        offset: int,
        type: str | None,
        status: str | None,
        login: str | None,
        group_name: str | None,
    ) -> list[TaskEntity]:
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

    async def get_tasks_order_by_created_at(
        self,
        limit: int,
        offset: int,
        type: str | None,
        status: str | None,
        login: str | None,
        group_name: str | None,
    ) -> list[TaskEntity]:
        stmt = select(TaskModel)

        if type is not None:
            stmt = stmt.where(TaskModel.type == type)
        if status is not None:
            stmt = stmt.where(TaskModel.status == status)
        if login is not None:
            stmt = stmt.where(TaskModel.login == login)
        if group_name is not None:
            stmt = stmt.where(TaskModel.group_name == group_name)

        stmt = stmt.order_by(TaskModel.created_at.desc()).limit(limit).offset(offset)

        result = await self._session.scalars(stmt)
        return [await self._convert_db_to_entity(task) for task in result.all()]
