from pocket_kai.application.interfaces.entities.task import TaskReader
from pocket_kai.domain.entitites.task import TaskEntity
from pocket_kai.infrastructure.kai_parser_api.schemas import TaskStatus, TaskType


class GetTasksInteractor:
    def __init__(
        self,
        task_gateway: TaskReader,
    ):
        self._task_gateway = task_gateway

    async def __call__(
        self,
        limit: int,
        offset: int,
        login: str | None,
        group_name: str | None,
        task_type: TaskType | None,
        task_status: TaskStatus | None,
    ) -> list[TaskEntity]:
        return await self._task_gateway.get_tasks(
            limit=limit,
            offset=offset,
            login=login,
            task_type=task_type,
            task_status=task_status,
            group_name=group_name,
        )
