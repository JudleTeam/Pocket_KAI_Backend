import datetime
from functools import cached_property
from typing import Any

from pydantic import BaseModel, ConfigDict, computed_field, field_validator, model_validator

from utils.kai_parser.schemas.common import LessonType, ParsedDatesStatus, WeekParity


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

    department_id: int | None
    department_name: str | None

    teacher_name: str
    teacher_login: str | None

    @field_validator('audience_number', 'building_number')
    @classmethod
    def remove_dashes(cls, value: str) -> str:
        return value.replace('-', '')

    @field_validator('audience_number', 'building_number', 'department_name')
    @classmethod
    def empty_to_none(cls, value: Any) -> Any | None:
        if not value:
            return None
        return value

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
        if not self.department_id and not self.department_name:
            self.department_id = self.department_name = None

        if self.teacher_name.lower() == 'преподаватель кафедры':
            self.teacher_login = None

        if self.parsed_lesson_type == LessonType.military_training:
            self.discipline_number = -1
            self.department_id = -1
            self.department_name = 'Военный учебный центр'

    @computed_field
    @cached_property
    def parsed_parity(self) -> WeekParity:
        dates = self.dates.replace('ё', 'e').lower()

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
        if 'физическая культура' in self.discipline_name.lower() and self.discipline_type.lower() == 'пр':
            return LessonType.physical_education

        if 'военная подготовка' == self.discipline_name.lower().strip():
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
    def parsed_dates(self) -> list[datetime.date] | None:
        sanitized_dates = self.sanitize_dates(self.dates)
        dates_str_list = sanitized_dates.split()

        try:
            current_year = datetime.date.today().year
            dates = [
                datetime.datetime.strptime(f'{date_str}.{current_year}', '%d.%m.%Y').date()
                for date_str in dates_str_list
            ]
        except ValueError:
            pass
        else:
            return dates

        try:
            dates = [
                datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
                for date_str in dates_str_list
            ]
        except ValueError:
            return None

        if not dates:
            return None

        return dates

    @computed_field
    @cached_property
    def parsed_dates_status(self) -> ParsedDatesStatus:
        good_parity_variants = (
            'неч', 'неч.нед', 'неч.нед.', 'нечет.нед.', 'нечетнаянеделя', 'неч.н', 'неч.н.', 'нечет.н', 'нечет.н.',
            'чет', 'чет.нед', 'чет.нед.', 'четнаянеделя', 'чет.н', 'чет.н.',
            'неч/чет', 'чет/неч', 'eжн', 'еженедельно'
        )
        processed_dates = self.dates.strip().replace('ё', 'е').replace(' ', '').lower()
        if processed_dates in good_parity_variants:
            return ParsedDatesStatus.GOOD

        if '/' in self.dates or 'подг' in self.dates.lower():
            return ParsedDatesStatus.NEED_CHECK

        if self.parsed_dates is not None:
            return ParsedDatesStatus.GOOD

        return ParsedDatesStatus.NEED_CHECK

    @computed_field
    @cached_property
    def end_time(self) -> datetime.time | None:
        if self.start_time is None:
            return None

        if self.parsed_lesson_type == LessonType.military_training:
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
        end_time = start_time + lesson_timedelta

        return (datetime.datetime.min + end_time).time()

    @staticmethod
    def sanitize_dates(dates: str) -> str:
        return (
            dates
            .replace('ё', 'е')
            .replace('нечет', '')
            .replace('неч', '')
            .replace('чет', '')
            .replace('2 подгр.', '')
            .replace('2 подгр', '')
            .replace('2 подг.', '')
            .replace('2 подг', '')
            .replace('1 подгр.', '')
            .replace('1 подгр', '')
            .replace('1 подг.', '')
            .replace('1 подг', '')
            .replace('()', ' ')
            .replace('/', ' ')
            .replace(';', ' ')
            .replace(',', ' ')
            .strip()
        )
