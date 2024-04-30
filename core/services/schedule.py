import datetime as dt
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from core.entities.lesson import LessonParity, LessonType
from core.services.base import BaseService
from database.models.kai import GroupLesson


class DisciplineRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    kai_id: int
    name: str


class DepartmentRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    kai_id: int
    name: str


class TeacherRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    login: str
    name: str

    department: DepartmentRead


class LessonRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    group_id: UUID
    number_of_day: int
    original_dates: str | None
    parsed_parity: LessonParity
    parsed_dates: list[dt.date] | None
    audience_number: str | None
    building_number: str | None
    original_lesson_type: str | None
    parsed_lesson_type: LessonType
    start_time: dt.time
    end_time: dt.time | None

    teacher: TeacherRead | None
    discipline: DisciplineRead


class DayResponse(BaseModel):
    date: dt.date
    parity: LessonParity = LessonParity.any
    lessons: list[LessonRead]


class ScheduleService(BaseService):
    async def _get_lessons_for_group(self, group_id: UUID | str):
        stmt = (
            select(GroupLesson)
            .where(
                GroupLesson.group_id == group_id
            )
        )

        records = await self.session.scalars(stmt)
        return records.all()

    def _filter_lessons_by_date(self, lessons: list[GroupLesson], date: dt.date) -> list[GroupLesson]:
        day_number = date.isoweekday()
        date_week_parity = LessonParity.get_parity_for_date(date)
        filtered_lessons = []

        for lesson in lessons:
            if lesson.number_of_day == day_number and lesson.parsed_parity in (LessonParity.any, date_week_parity):
                filtered_lessons.append(lesson)

        return filtered_lessons

    async def get_group_schedule_with_dates(self, group_id: UUID | str, date_from: dt.date, days: int):
        dates = [date_from + dt.timedelta(days=x) for x in range(days + 1)]
        group_lessons = await self._get_lessons_for_group(group_id)

        schedule = []
        for date in dates:
            parity = LessonParity.get_parity_for_date(date)
            schedule_day = DayResponse(
                date=date,
                parity=parity,
                lessons=[
                    LessonRead.model_validate(lesson)
                    for lesson in self._filter_lessons_by_date(group_lessons, date)
                ],
            )
            schedule.append(schedule_day)

        return schedule
