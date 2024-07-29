import dataclasses

import datetime

from pydantic import BaseModel

from utils.common import LessonType, ParsedDatesStatus, WeekParity
from utils.pocket_kai_api.schemas import PocketKaiGroup


class ParsedGroup(BaseModel):
    forma: str
    name: str
    id: int

    def __eq__(self, other):
        if isinstance(other, PocketKaiGroup):
            return self.id == other.kai_id


class ParsedGroupSchedule(BaseModel):
    parsed_at: datetime.datetime
    group_kai_id: int
    lessons: list['ParsedLesson']


class ParsedLesson(BaseModel):
    day_number: int
    start_time: datetime.time | None
    end_time: datetime.time | None
    dates: str | None
    parsed_dates: list[datetime.date] | None
    parsed_dates_status: ParsedDatesStatus
    parsed_parity: WeekParity
    parsed_lesson_type: LessonType

    discipline_name: str
    discipline_type: str
    discipline_number: int

    audience_number: str | None
    building_number: str | None

    department_id: int | None
    department_name: str | None

    teacher_name: str
    teacher_login: str | None


@dataclasses.dataclass
class YearDataForGroup:
    academic_year: str
    academic_year_half: int
    semester: int


class ParsedExam(BaseModel):
    date: str
    parsed_date: datetime.date | None
    time: datetime.time
    discipline_name: str
    discipline_number: int
    audience_number: str | None
    building_number: str | None
    teacher_name: str
    teacher_login: str | None


class ParsedGroupExams(BaseModel):
    parsed_at: datetime.datetime
    year_data: YearDataForGroup
    group_kai_id: int
    parsed_exams: list[ParsedExam]
