import datetime as dt
from enum import Enum
from typing import Union


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
    odd = 'odd'
    even = 'even'
    any = 'any'

    @classmethod
    def get_parity_for_date(cls, date: dt.date) -> Union['WeekParity.even', 'WeekParity.odd']:
        if int(date.strftime("%V")) % 2 == 1:
            return cls.odd
        return cls.even


class ParsedDatesStatus(str, Enum):
    GOOD = 'good'
    NEED_CHECK = 'need_check'
