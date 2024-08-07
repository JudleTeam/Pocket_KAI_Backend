from uuid import UUID

from datetime import datetime

from pydantic import BaseModel

from pocket_kai.controllers.schemas.department import DepartmentRead
from pocket_kai.controllers.schemas.institute import InstituteRead
from pocket_kai.controllers.schemas.profile import ProfileRead
from pocket_kai.controllers.schemas.speciality import SpecialityRead


class ShortGroupRead(BaseModel):
    id: UUID

    kai_id: int
    group_name: str

    is_verified: bool
    parsed_at: datetime | None

    schedule_parsed_at: datetime | None
    exams_parsed_at: datetime | None


class FullGroupRead(BaseModel):
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

    speciality: SpecialityRead | None
    profile: ProfileRead | None
    department: DepartmentRead | None
    institute: InstituteRead | None


class GroupCreate(BaseModel):
    group_name: str
    kai_id: int


class GroupUpdate(BaseModel):
    kai_id: int
    group_leader_id: UUID | None
    pinned_text: str | None
    group_name: str

    is_verified: bool
    verified_at: datetime | None
    parsed_at: datetime | None

    schedule_parsed_at: datetime | None
    exams_parsed_at: datetime | None

    speciality_id: UUID | None
    profile_id: UUID | None
    department_id: UUID | None
    institute_id: UUID | None

    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None


class GroupPatch(BaseModel):
    kai_id: int = None
    group_leader_id: UUID | None = None
    pinned_text: str | None = None
    group_name: str = None

    is_verified: bool = None
    verified_at: datetime | None = None
    parsed_at: datetime | None = None

    schedule_parsed_at: datetime | None = None
    exams_parsed_at: datetime | None = None

    speciality_id: UUID | None = None
    profile_id: UUID | None = None
    department_id: UUID | None = None
    institute_id: UUID | None = None

    syllabus_url: str | None = None
    educational_program_url: str | None = None
    study_schedule_url: str | None = None


class UpdateDocumentsRequest(BaseModel):
    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None
