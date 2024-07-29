from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel

from utils.common import LessonType, ParsedDatesStatus, WeekParity


class PocketKaiGroup(BaseModel):
    id: UUID
    kai_id: int

    group_leader_id: UUID | None
    pinned_text: str | None
    group_name: str

    is_verified: bool
    verified_at: datetime | None
    created_at: datetime
    parsed_at: datetime | None

    schedule_parsed_at: datetime | None
    exams_parsed_at: datetime | None

    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None


class PocketKaiDepartment(BaseModel):
    id: UUID
    created_at: datetime
    kai_id: int
    name: str


class PocketKaiTeacher(BaseModel):
    id: UUID
    created_at: datetime
    login: str
    name: str


class PocketKaiDiscipline(BaseModel):
    id: UUID
    created_at: datetime
    kai_id: int
    name: str


class PocketKaiLesson(BaseModel):
    id: UUID
    created_at: datetime
    group_id: UUID
    number_of_day: int
    original_dates: str | None
    parsed_parity: WeekParity
    parsed_dates: list[date] | None
    parsed_dates_status: ParsedDatesStatus
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType
    start_time: time | None
    end_time: time | None

    teacher: PocketKaiTeacher | None
    department: PocketKaiDepartment | None
    discipline: PocketKaiDiscipline


class PocketKaiExam(BaseModel):
    id: UUID
    created_at: datetime
    original_date: str
    time: time
    audience_number: str | None
    building_number: str | None
    parsed_date: date | None
    academic_year: str
    academic_year_half: int
    semester: int | None
    group_id: UUID

    teacher: PocketKaiTeacher | None
    discipline: PocketKaiDiscipline
