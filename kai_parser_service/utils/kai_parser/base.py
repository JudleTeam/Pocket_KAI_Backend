from abc import abstractmethod
from typing import Protocol

from utils.kai_parser.schemas.group import ParsedGroup
from utils.kai_parser.schemas.lesson import ParsedLesson


class KaiParserBase(Protocol):
    @abstractmethod
    async def parse_groups(self) -> list[ParsedGroup]:
        raise NotImplementedError

    @abstractmethod
    async def parse_group_schedule(self, group_kai_id: int) -> list[ParsedLesson]:
        raise NotImplementedError


