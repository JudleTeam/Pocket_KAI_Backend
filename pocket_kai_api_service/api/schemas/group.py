from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TunedModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class ShortGroupRead(TunedModel):
    id: UUID

    kai_id: int
    group_name: str

    is_verified: bool
    parsed_at: datetime | None

    schedule_parsed_at: datetime | None


class FullGroupRead(TunedModel):
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

    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None

    # speciality: SpecialityRead
    # profile: ProfileRead
    # department: DepartmentRead
    # institute: InstituteRead


class GroupCreate(TunedModel):
    group_name: str
    kai_id: int


class GroupUpdate(TunedModel):
    kai_id: int
    group_leader_id: UUID | None
    pinned_text: str | None
    group_name: str

    is_verified: bool
    verified_at: datetime | None
    parsed_at: datetime | None

    schedule_parsed_at: datetime | None

    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None
