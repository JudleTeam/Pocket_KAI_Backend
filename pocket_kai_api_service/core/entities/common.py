import datetime as dt
from enum import Enum


class LessonType(str, Enum):
    lecture = 'lecture'
    practice = 'practice'
    laboratory_work = 'lab_work'
    consultation = 'consult'
    physical_education = 'phys_edu'
    course_work = 'course_work'
    individual_task = 'ind_task'
    military_training = 'military'
    unknown = 'unknown'


class WeekParity(str, Enum):
    ODD = 'odd'  # Нечётная
    EVEN = 'even'  # Чётная
    ANY = 'any'  # Нечётная / Чётная

    @classmethod
    def get_parity_for_date(
        cls,
        date: dt.date,
    ) -> 'WeekParity':
        """
        Value could be either ODD or EVEN
        """
        if int(date.strftime('%V')) % 2 == 1:
            return cls(cls.ODD)
        return cls(cls.EVEN)

    def to_int(self) -> int:
        if self.value == self.ODD:
            return 1

        if self.value == self.EVEN:
            return 0

        raise ValueError(
            'WeekParity should be either ODD or EVEN to be converted to int',
        )


class ParsedDatesStatus(str, Enum):
    GOOD = 'good'
    NEED_CHECK = 'need_check'
