import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from utils.kai_parser.schemas.group import Group, Documents


class BaseUser(BaseModel):
    full_name: str
    phone: str | None
    email: str


class UserInfo(BaseUser):
    sex: str
    birthday: datetime.date


class UserAbout(BaseModel):
    # TODO: update attribute names
    groupNum: int
    competitionType: str
    specCode: str
    kafName: str
    programForm: str
    profileId: int
    numDog: int | None
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

    @field_validator('numDog', mode='before')
    @classmethod
    def validate_num_dog(cls, num_dog: str):
        num_dog = num_dog.strip()
        if not num_dog.isdigit():
            return None
        return int(num_dog)

    class Config:
        str_strip_whitespace = True


class FullUserData(BaseModel):
    user_info: UserInfo
    user_about: UserAbout
    group: 'Group'
    documents: 'Documents'
