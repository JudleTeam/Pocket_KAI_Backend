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
