from datetime import date, time

import dataclasses
from pydantic import BaseModel

from pocket_kai.domain.common import LessonType, ParsedDatesStatus, WeekParity
from pocket_kai.domain.entitites.department import DepartmentEntity
from pocket_kai.domain.entitites.discipline import DisciplineEntity
from pocket_kai.domain.entitites.lesson import LessonEntity
from pocket_kai.domain.entitites.teacher import TeacherEntity


@dataclasses.dataclass(slots=True)
class NewLessonDTO:
    number_of_day: int
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[date] | None
    parsed_dates_status: ParsedDatesStatus
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType | None
    start_time: time | None
    end_time: time | None

    discipline_id: str
    teacher_id: str | None
    department_id: str | None
    group_id: str


class LessonPatchDTO(BaseModel):
    number_of_day: int = None
    original_dates: str | None = None
    parsed_parity: WeekParity = None
    parsed_dates: list[date] | None = None
    parsed_dates_status: ParsedDatesStatus = None
    audience_number: str | None = None
    building_number: str | None = None
    original_lesson_type: str | None = None
    parsed_lesson_type: LessonType | None = None
    start_time: time | None = None
    end_time: time | None = None

    discipline_id: str = None
    teacher_id: str | None = None
    department_id: str | None = None
    group_id: str = None


@dataclasses.dataclass(slots=True)
class LessonExtendedDTO(LessonEntity):
    # TODO: возможно не очень правильно тут использовать Entity
    teacher: TeacherEntity | None
    department: DepartmentEntity | None
    discipline: DisciplineEntity
