import datetime
from functools import cached_property

from pydantic import BaseModel, ConfigDict, computed_field, field_validator, model_validator

from utils.kai_parser.schemas.common import LessonType, WeekParity


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

    audience_number: str | None
    building_number: str | None

    department_id: int
    department_name: str

    teacher_name: str
    teacher_login: str | None

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

    @model_validator(mode='after')
    def validate_model(self):
        if self.teacher_name.lower() == 'преподаватель кафедры':
            self.teacher_login = None

        if self.parsed_lesson_type == LessonType.military_training:
            self.discipline_number = -1
            self.department_id = -1
            self.building_number = None
            self.audience_number = None

    @computed_field
    @cached_property
    def parsed_parity(self) -> WeekParity:
        dates = self.dates.replace('ё', 'e')

        # 'нея' - typo.
        if 'нечет' in dates or 'неч' in dates or 'нея' in dates:
            odd = True
            dates = dates.replace('нечет', '')
        else:
            odd = False

        even = 'чет' in dates

        if odd and not even:
            return WeekParity.odd
        if even and not odd:
            return WeekParity.even
        return WeekParity.any

    @computed_field
    @cached_property
    def parsed_lesson_type(self) -> LessonType:
        if 'физическая культура' in self.discipline_name.lower():
            return LessonType.physical_education

        if 'военная' in self.discipline_name.lower():
            return LessonType.military_training

        lesson_type_mapping = {
            'лек': LessonType.lecture,
            'пр': LessonType.practice,
            'л.р.': LessonType.laboratory_work,
            'конс': LessonType.consultation,
            'к.р.': LessonType.course_work,
            'и.д.': LessonType.individual_task,
        }

        return lesson_type_mapping.get(self.discipline_type.strip().lower(), LessonType.unknown)

    @computed_field
    @cached_property
    def end_time(self) -> datetime.time | None:
        if self.start_time is None:
            return None

        if self.parsed_lesson_type == LessonType.military_training:
            return datetime.time(hour=18, minute=0)

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
        end_time = start_time + lesson_timedelta

        return (datetime.datetime.min + end_time).time()
