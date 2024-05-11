import datetime

from pydantic import BaseModel, ConfigDict

from utils.kai_parser.schemas.common import LessonType, WeekParity


class LessonRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    day_number: int
    start_time: datetime.time | None
    end_time: datetime.time | None
    dates: str
    parsed_parity: WeekParity
    parsed_lesson_type: LessonType

    discipline_name: str
    discipline_type: str
    discipline_number: int

    audience_number: str | None
    building_number: str | None

    department_id: int
    department_name: str

    teacher_name: str
    teacher_login: str | None
