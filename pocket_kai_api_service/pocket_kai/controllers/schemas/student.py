from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime


class StudentRead(BaseModel):
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


class GroupMemberRead(BaseModel):
    id: UUID
    kai_id: int | None
    position: int | None
    is_leader: bool
    full_name: str
    email: str


class GroupMember(BaseModel):
    number: int
    is_leader: bool
    full_name: str
    phone: str | None
    email: str


class AddGroupMembersRequest(BaseModel):
    group_name: str
    students: list[GroupMember]
