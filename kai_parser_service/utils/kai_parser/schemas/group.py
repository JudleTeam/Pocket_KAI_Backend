from typing import TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from utils.kai_parser.schemas.user import BaseUser


class ParsedGroup(BaseModel):
    forma: str
    name: str
    id: int


class Group(BaseModel):
    members: list['BaseUser']
    leader_num: int | None


class Documents(BaseModel):
    syllabus: str | None
    educational_program: str | None
    study_schedule: str | None
