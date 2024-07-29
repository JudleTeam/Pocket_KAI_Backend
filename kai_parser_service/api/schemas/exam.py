import datetime as dt

from pydantic import BaseModel

from utils.kai_parser.schemas.exam import YearDataForGroup


class ExamRead(BaseModel):
    date: str
    parsed_date: dt.date | None
    time: dt.time
    discipline_name: str
    discipline_number: int
    audience_number: int | None
    building_number: int | None
    teacher_name: str
    teacher_login: str | None


class GroupExamsResponse(BaseModel):
    parsed_at: dt.datetime
    year_data: YearDataForGroup
    group_kai_id: int
    parsed_exams: list[ExamRead]
