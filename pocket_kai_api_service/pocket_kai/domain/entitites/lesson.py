import dataclasses
import datetime as dt
from uuid import UUID

from pocket_kai.domain.common import LessonType, ParsedDatesStatus, WeekParity


@dataclasses.dataclass(slots=True)
class LessonEntity:
    id: str
    created_at: dt.datetime
    number_of_day: int
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[dt.date] | None
    parsed_dates_status: ParsedDatesStatus

    start_time: dt.time | None
    end_time: dt.time | None

    audience_number: str | None
    building_number: str | None

    original_lesson_type: str | None
    parsed_lesson_type: LessonType

    group_id: UUID
    discipline_id: UUID
    department_id: UUID | None
    teacher_id: UUID | None
