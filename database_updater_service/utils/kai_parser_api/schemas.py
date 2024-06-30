import datetime

from pydantic import BaseModel

from utils.common import LessonType, ParsedDatesStatus, WeekParity
from utils.pocket_kai_api.schemas import PocketKaiGroup, PocketKaiLesson


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
    dates: str
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

    def __eq__(self, other):
        if isinstance(other, PocketKaiLesson):
            return (
                self.day_number == other.number_of_day and
                self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.dates == other.original_dates and
                self.parsed_dates == other.parsed_dates and
                self.parsed_dates_status == other.parsed_dates_status and
                self.parsed_parity == other.parsed_parity and
                self.parsed_lesson_type == other.parsed_lesson_type and
                self.discipline_type == other.original_lesson_type and
                self.discipline_number == other.discipline.kai_id and
                self.audience_number == other.audience_number and
                self.building_number == other.building_number and
                self.department_id == other.department.kai_id and
                self.teacher_login == other.teacher.login if other.teacher else None
            )
