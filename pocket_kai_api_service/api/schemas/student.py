from uuid import UUID
from datetime import date, datetime

from api.schemas.common import TunedModel


class StudentRead(TunedModel):
    id: UUID
    created_at: datetime
    kai_id: int | None
    position: int | None
    login: str | None
    full_name: str
    phone: str | None
    email: str
    sex: str | None
    birthday: date | None
    is_leader: bool
    zach_number: str | None
    competition_type: str | None
    contract_number: str | None
    edu_level: str | None
    edu_cycle: str | None
    edu_qualification: str | None
    program_form: str | None
    status: str | None

    group_id: UUID | None
    user_id: UUID | None


class GroupMember(TunedModel):
    number: int
    is_leader: bool
    full_name: str
    phone: str | None
    email: str


class AddGroupMembersRequest(TunedModel):
    group_name: str
    students: list[GroupMember]
