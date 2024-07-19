import dataclasses
import datetime as dt


@dataclasses.dataclass(slots=True)
class GroupEntity:
    id: str
    created_at: dt.datetime
    kai_id: int
    group_leader_id: str | None
    pinned_text: str | None
    group_name: str

    is_verified: bool
    verified_at: dt.datetime | None
    parsed_at: dt.datetime | None

    schedule_parsed_at: dt.datetime | None

    syllabus_url: str | None
    educational_program_url: str | None
    study_schedule_url: str | None

    speciality_id: str | None
    profile_id: str | None
    department_id: str | None
    institute_id: str | None
