import dataclasses

from datetime import datetime

from pydantic import BaseModel

from pocket_kai.domain.entitites.department import DepartmentEntity
from pocket_kai.domain.entitites.group import GroupEntity
from pocket_kai.domain.entitites.institute import InstituteEntity
from pocket_kai.domain.entitites.profile import ProfileEntity
from pocket_kai.domain.entitites.speciality import SpecialityEntity


@dataclasses.dataclass(slots=True)
class NewGroupDTO:
    group_name: str
    kai_id: int


class GroupPatchDTO(BaseModel):
    kai_id: int = None
    group_leader_id: str | None = None
    pinned_text: str | None = None
    group_name: str = None

    is_verified: bool = None
    verified_at: datetime | None = None
    parsed_at: datetime | None = None

    schedule_parsed_at: datetime | None = None

    speciality_id: str | None = None
    profile_id: str | None = None
    department_id: str | None = None
    institute_id: str | None = None

    syllabus_url: str | None = None
    educational_program_url: str | None = None
    study_schedule_url: str | None = None


@dataclasses.dataclass(slots=True)
class GroupExtendedDTO(GroupEntity):
    profile: ProfileEntity | None
    speciality: SpecialityEntity | None
    department: DepartmentEntity | None
    institute: InstituteEntity | None
