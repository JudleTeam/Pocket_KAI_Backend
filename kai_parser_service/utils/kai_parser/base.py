from abc import abstractmethod
from typing import Protocol

from utils.kai_parser.schemas.group import ParsedGroup
from utils.kai_parser.schemas.schedule import ParsedGroupSchedule


class KaiParserBase(Protocol):
    @abstractmethod
    async def parse_groups(self) -> list[ParsedGroup]:
        raise NotImplementedError

    @abstractmethod
    async def parse_group_schedule(self, group_kai_id: int) -> ParsedGroupSchedule:
        raise NotImplementedError
