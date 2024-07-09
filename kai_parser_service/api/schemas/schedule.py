import datetime

from pydantic import BaseModel, ConfigDict

from utils.kai_parser.schemas.common import LessonType, ParsedDatesStatus, WeekParity


class GroupScheduleResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    parsed_at: datetime.datetime
    group_kai_id: int
    lessons: list['LessonRead']


class LessonRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

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
