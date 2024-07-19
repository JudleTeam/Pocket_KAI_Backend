from abc import abstractmethod

from typing import Protocol

from pocket_kai.infrastructure.kai_parser_api.schemas import TaskStatus, TaskType


class TaskReader(Protocol):
    @abstractmethod
    async def get_tasks(
        self,
        limit: int,
        offset: int,
        login: str | None,
        group_name: str | None,
        task_type: TaskType | None,
        task_status: TaskStatus | None,
    ):
        raise NotImplementedError
