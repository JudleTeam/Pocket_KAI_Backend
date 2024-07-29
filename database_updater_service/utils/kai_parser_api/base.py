from abc import abstractmethod
from typing import Protocol

from utils.kai_parser_api.schemas import (
    ParsedGroup,
    ParsedGroupExams,
    ParsedGroupSchedule,
)


class KaiParserApiBase(Protocol):
    @abstractmethod
    async def get_groups(self) -> list[ParsedGroup]:
        raise NotImplementedError

    @abstractmethod
    async def get_group_schedule(self, group_kai_id: int) -> ParsedGroupSchedule:
        raise NotImplementedError

    @abstractmethod
    async def get_group_exams(
        self,
        group_kai_id: int,
        group_name: str,
    ) -> ParsedGroupExams:
        raise NotImplementedError
