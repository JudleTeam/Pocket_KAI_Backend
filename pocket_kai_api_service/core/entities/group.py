import datetime as dt
from uuid import UUID

from core.entities.base import BaseEntity


class GroupEntity(BaseEntity):
    kai_id: int
    group_leader_id: UUID | None
    pinned_text: str | None
    group_name: str

    is_verified: bool
    verified_at: dt.datetime | None
    parsed_at: dt.datetime | None

    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None

    # speciality: SpecialityEntity | None
    # profile: ProfileEntity | None
    # departament: DepartmentEntity | None
    # institute: InstituteEntity| None
