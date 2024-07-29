import dataclasses
import datetime as dt

from pocket_kai.domain.entitites.discipline import DisciplineEntity
from pocket_kai.domain.entitites.exam import ExamEntity
from pocket_kai.domain.entitites.teacher import TeacherEntity


@dataclasses.dataclass(slots=True)
class NewExamDTO:
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


@dataclasses.dataclass(slots=True)
class UpdateExamDTO:
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


@dataclasses.dataclass(slots=True)
class ExamExtendedDTO(ExamEntity):
    teacher: TeacherEntity
    discipline: DisciplineEntity
