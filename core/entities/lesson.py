import datetime
from enum import Enum
from typing import Self, Union


class LessonType(str, Enum):
    lecture = 'lecture'
    practice = 'practice'
    laboratory_work = 'lab_work'
    consultation = 'consult'
    physical_education = 'phys_edu'
    course_work = 'course_work'
    individual_task = 'ind_task'
    unknown = 'unknown'


class LessonParity(str, Enum):
    odd = 'odd'
    even = 'even'
    any = 'any'

    @classmethod
    def get_parity_for_date(cls, date: datetime.date) -> Union['LessonParity.even', 'LessonParity.odd']:
        if int(date.strftime("%V")) % 2 == 1:
            return cls.odd
        return cls.even
