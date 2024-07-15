from enum import Enum

from uuid import UUID

import datetime

from pydantic import BaseModel


class GroupMember(BaseModel):
    number: int
    is_leader: bool
    full_name: str
    phone: str | None
    email: str


class UserInfo(BaseModel):
    full_name: str
    phone: str | None
    email: str
    sex: str
    birthday: datetime.date


class UserAbout(BaseModel):
    groupNum: int
    competitionType: str
    specCode: str
    kafName: str
    programForm: str
    profileId: int
    numDog: str | None
    rukFio: str | None
    eduLevel: str
    rabProfile: str | None
    oval: str | None
    eduQualif: str
    predpr: str | None
    status: str
    instId: int
    studId: int
    instName: str
    tabName: str
    groupId: int
    eduCycle: str
    specName: str
    specId: int
    zach: str
    profileName: str
    dateDog: str | None
    kafId: int
    rabTheme: str | None


class TaskType(str, Enum):
    """Task type enum."""

    GROUP_MEMBERS = 'group_members'
    GROUP_DOCUMENTS = 'group_documents'


class TaskStatus(str, Enum):
    """Task status enum."""

    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'


class TaskSchema(BaseModel):
    id: UUID
    created_at: datetime.datetime
    type: TaskType
    status: TaskStatus
    login: str | None
    group_name: str | None
    errors: str | None
    ended_at: datetime.datetime | None
