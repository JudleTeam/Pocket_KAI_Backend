from pocket_kai.application.interfaces.entities.task import TaskReader
from pocket_kai.application.interfaces.kai_parser_api import KaiParserApiProtocol
from pocket_kai.infrastructure.kai_parser_api.schemas import TaskStatus, TaskType


class TaskGateway(TaskReader):
    def __init__(self, kai_parser_api: KaiParserApiProtocol):
        self._kai_parser_api = kai_parser_api

    async def get_tasks(
        self,
        limit: int,
        offset: int,
        login: str | None,
        group_name: str | None,
        task_type: TaskType | None,
        task_status: TaskStatus | None,
    ):
        return await self._kai_parser_api.get_tasks(
            limit=limit,
            offset=offset,
            login=login,
            group_name=group_name,
            type=task_type,
            status=task_status,
        )
