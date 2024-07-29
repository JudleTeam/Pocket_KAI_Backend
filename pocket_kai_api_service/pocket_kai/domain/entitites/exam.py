import dataclasses
import datetime as dt


@dataclasses.dataclass(slots=True)
class ExamEntity:
    id: str
    created_at: dt.datetime
    original_date: str
    time: dt.time
    audience_number: str | None
    building_number: str | None
    parsed_date: dt.date | None
    academic_year: str
    academic_year_half: int
    semester: int | None
    discipline_id: str
    teacher_id: str | None
    group_id: str
