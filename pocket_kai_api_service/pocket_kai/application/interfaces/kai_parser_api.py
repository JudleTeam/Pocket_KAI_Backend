from abc import abstractmethod

from typing import Protocol

from pocket_kai.infrastructure.kai_parser_api.schemas import (
    TaskSchema,
    TaskStatus,
    TaskType,
    UserAbout,
    UserInfo,
)


class KaiParserApiProtocol(Protocol):
    @abstractmethod
    async def kai_login(
        self,
        username,
        password,
        parse_user_data=True,
    ) -> tuple[UserAbout, UserInfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_tasks(
        self,
        limit: int,
        offset: int,
        group_name: str | None,
        login: str | None,
        type: TaskType | None = None,
        status: TaskStatus | None = None,
    ) -> list[TaskSchema]:
        raise NotImplementedError
