from abc import abstractmethod
from typing import Protocol

from utils.kai_parser_api.schemas import ParsedGroup, ParsedGroupSchedule


class KaiParserApiBase(Protocol):
    @abstractmethod
    async def get_groups(self) -> list[ParsedGroup]:
        raise NotImplementedError

    @abstractmethod
    async def get_group_schedule(self, group_kai_id: int) -> ParsedGroupSchedule:
        raise NotImplementedError
