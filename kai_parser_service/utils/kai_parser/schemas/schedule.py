import datetime
from dataclasses import dataclass

from utils.kai_parser.schemas.lesson import ParsedLesson


# При использовании модели pydantic, lessons превращается в список из None
@dataclass
class ParsedGroupSchedule:
    parsed_at: datetime.datetime
    group_kai_id: int
    lessons: list[ParsedLesson]
