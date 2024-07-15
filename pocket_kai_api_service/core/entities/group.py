import datetime as dt
from uuid import UUID

from core.entities.base import BaseEntity
from core.entities.department import DepartmentEntity
from core.entities.institute import InstituteEntity
from core.entities.profile import ProfileEntity
from core.entities.speciality import SpecialityEntity


class GroupEntity(BaseEntity):
    kai_id: int
    group_leader_id: UUID | None
    pinned_text: str | None
    group_name: str

    is_verified: bool = False
    verified_at: dt.datetime | None
    parsed_at: dt.datetime | None

    schedule_parsed_at: dt.datetime | None

    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None

    speciality_id: UUID | None
    profile_id: UUID | None
    department_id: UUID | None
    institute_id: UUID | None

    speciality: SpecialityEntity | None = None
    profile: ProfileEntity | None = None
    department: DepartmentEntity | None = None
    institute: InstituteEntity | None = None
