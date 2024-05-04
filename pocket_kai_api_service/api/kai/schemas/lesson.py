from uuid import UUID
import datetime as dt

from pydantic import BaseModel, ConfigDict

from api.kai.schemas.discipline import DisciplineRead
from api.kai.schemas.teacher import TeacherRead
from core.entities.lesson import LessonType, WeekParity


class LessonRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    group_id: UUID
    number_of_day: int
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[dt.date] | None
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType
    start_time: dt.time
    end_time: dt.time | None

    teacher: TeacherRead | None
    discipline: DisciplineRead
