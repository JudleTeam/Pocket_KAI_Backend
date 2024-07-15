from api.schemas.task import TaskRead
from utils.kai_parser_api.api import KaiParserApi


class TaskUseCase:
    def __init__(
        self,
        kai_parser_api: KaiParserApi,
    ):
        self.kai_parser_api = kai_parser_api

    async def get_tasks(
        self,
        limit: int,
        offset: int,
        group_name: str | None,
        login: str | None,
    ) -> list[TaskRead]:
        tasks = await self.kai_parser_api.get_tasks(
            limit=limit,
            offset=offset,
            group_name=group_name,
            login=login,
        )
        return [TaskRead.model_validate(task) for task in tasks]
