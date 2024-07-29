import dataclasses
import datetime as dt

from pydantic import BaseModel, ConfigDict, computed_field, field_validator


class ParsedExam(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    date: str
    time: dt.time
    discipline_name: str
    discipline_number: int
    teacher_name: str
    teacher_login: str | None
    audience_number: str | None
    building_number: str | None

    @field_validator('time', mode='before')
    @classmethod
    def parse_time_from_str(cls, str_time: str) -> dt.time | None:
        try:
            return dt.datetime.strptime(str_time.strip(), '%H:%M').time()
        except ValueError:
            return None

    @field_validator('teacher_name')
    @classmethod
    def title_str(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            return value.title()
        return value

    @computed_field
    @property
    def parsed_date(self) -> dt.date | None:
        try:
            return dt.datetime.strptime(self.date, '%d.%m.%Y').date()
        except ValueError:
            return None


@dataclasses.dataclass
class YearDataForGroup:
    academic_year: str
    academic_year_half: int
    semester: int


@dataclasses.dataclass
class ParsedGroupExams:
    parsed_at: dt.datetime
    year_data: YearDataForGroup
    group_kai_id: int
    parsed_exams: list[ParsedExam]
