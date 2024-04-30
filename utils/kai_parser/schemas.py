import datetime
from functools import cached_property

from pydantic import BaseModel, ConfigDict, field_validator

from core.entities.lesson import LessonParity, LessonType


class KaiApiError(Exception):
    """Can't get data from Kai site"""


class ParsingError(Exception):
    """Can't parse data from kai.ru"""


class BadCredentials(Exception):
    """Bad credentials for login"""


class ParsedGroup(BaseModel):
    forma: str
    name: str
    id: int


class Teacher(BaseModel):
    type: str
    lesson_name: str
    teacher_full_name: str


class ParsedLesson(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    day_number: int
    start_time: datetime.time | None
    dates: str

    discipline_name: str
    discipline_type: str
    discipline_number: int

    audience_number: str
    building_number: str

    department_id: int
    department_name: str

    teacher_name: str
    teacher_login: str

    @field_validator('audience_number')
    @classmethod
    def remove_dashes(cls, value: str) -> str:
        return value.replace('-', '')

    @field_validator('teacher_name')
    @classmethod
    def title_str(cls, value: str) -> str:
        return value.title()

    @field_validator('start_time', mode='before')
    @classmethod
    def parse_time_from_str(cls, str_time: str) -> datetime.time | None:
        try:
            return datetime.datetime.strptime(str_time.strip(), '%H:%M').time()
        except ValueError:
            return None

    @cached_property
    def parsed_parity(self) -> LessonParity:
        dates = self.dates.replace('ё', 'e')

        # 'нея' - typo.
        if 'нечет' in dates or 'неч' in dates or 'нея' in dates:
            odd = True
            dates = dates.replace('нечет', '')
        else:
            odd = False

        even = 'чет' in dates

        if odd and not even:
            return LessonParity.odd
        if even and not odd:
            return LessonParity.even
        return LessonParity.any

    @cached_property
    def parsed_lesson_type(self) -> LessonType:
        if 'физическая культура' in self.discipline_name.lower():
            return LessonType.physical_education

        match self.discipline_type:
            case 'лек':
                return LessonType.lecture
            case 'пр':
                return LessonType.practice
            case 'л.р.':
                return LessonType.laboratory_work
            case 'конс':
                return LessonType.consultation
            case 'к.р.':
                return LessonType.course_work
            case 'и.д.':
                return LessonType.individual_task
            case _:
                return LessonType.unknown

    @cached_property
    def end_time(self) -> datetime.time | None:
        if self.start_time is None:
            return None

        start_times = (
            datetime.timedelta(hours=8, minutes=00),
            datetime.timedelta(hours=9, minutes=40),
            datetime.timedelta(hours=11, minutes=20),
            datetime.timedelta(hours=13, minutes=30),
            datetime.timedelta(hours=15, minutes=10),
            datetime.timedelta(hours=16, minutes=50),
            datetime.timedelta(hours=18, minutes=25),
            datetime.timedelta(hours=20, minutes=00)
        )

        start_time = datetime.timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)

        if start_time not in start_times:
            return None

        lesson_timedelta = datetime.timedelta(hours=1, minutes=30)

        # Если лаб. работы по 2 пары сразу:
        # if lesson_type == 'л.р.':
        #     next_lesson_ind = start_times.index(start_time) + 1
        #     if next_lesson_ind > len(start_times) - 1:
        #         # Бывают лабораторные работы в 20:00, видимо они длятся одну пару
        #         next_lesson_ind = len(start_times) - 1
        #     end_time = start_times[next_lesson_ind] + lesson_timedelta
        # else:
        #     end_time = start_time + lesson_timedelta

        end_time = start_time + lesson_timedelta

        return (datetime.datetime.min + end_time).time()


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


class Group(BaseModel):
    members: list[BaseUser]
    leader_num: int | None


class Documents(BaseModel):
    syllabus: str | None
    educational_program: str | None
    study_schedule: str | None


class FullUserData(BaseModel):
    user_info: UserInfo
    user_about: UserAbout
    group: Group
    documents: Documents
