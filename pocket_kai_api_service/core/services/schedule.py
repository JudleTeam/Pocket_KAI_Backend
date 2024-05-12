import datetime as dt
from abc import ABC, abstractmethod
from uuid import UUID

from core.entities.group import GroupEntity
from core.entities.lesson import LessonEntity
from core.entities.common import WeekParity
from core.entities.schedule import DayEntity, ScheduleEntity, WeekEntity
from core.services.group import GroupServiceBase
from core.services.lesson import LessonServiceBase


class ScheduleServiceBase(ABC):
    def __init__(
        self,
        lesson_service: LessonServiceBase,
        group_service: GroupServiceBase
    ):
        self._lesson_service = lesson_service
        self._group_service = group_service

    @abstractmethod
    async def get_schedule_with_dates_by_group_id(
        self,
        group_id: UUID,
        date_from: dt.date,
        days_count: int
    ) -> list[DayEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_schedule_with_dates_by_group_name(
        self,
        group_name: str,
        date_from: dt.date,
        days_count: int
    ) -> list[DayEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_schedule_with_week_days_by_group_id(
        self,
        group_id: UUID,
        week_parity: WeekParity
    ) -> WeekEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_schedule_with_week_days_by_group_name(
        self,
        group_name: str,
        week_parity: WeekParity
    ) -> WeekEntity:
        raise NotImplementedError


class ScheduleService(ScheduleServiceBase):
    @staticmethod
    def _filter_lessons_by_date(group_lessons: list[LessonEntity], date: dt.date) -> list[LessonEntity]:
        day_number = date.isoweekday()
        date_week_parity = WeekParity.get_parity_for_date(date)
        filtered_lessons = []

        for lesson in group_lessons:
            if lesson.parsed_dates:
                if date in lesson.parsed_dates:
                    filtered_lessons.append(lesson)
            elif lesson.number_of_day == day_number and lesson.parsed_parity in (WeekParity.any, date_week_parity):
                filtered_lessons.append(lesson)

        return filtered_lessons

    async def _get_schedule_with_week_days_by_group(self, group: GroupEntity, week_parity: WeekParity) -> WeekEntity:
        group_lessons = await self._lesson_service.get_by_group_id(group.id, week_parity=week_parity)

        lessons_by_week_days = {
            'monday'   : [],
            'tuesday'  : [],
            'wednesday': [],
            'thursday' : [],
            'friday'   : [],
            'saturday' : [],
            'sunday'   : []
        }

        day_mapping = {
            1: 'monday',
            2: 'tuesday',
            3: 'wednesday',
            4: 'thursday',
            5: 'friday',
            6: 'saturday',
            7: 'sunday'
        }

        for lesson in group_lessons:
            day = day_mapping.get(lesson.number_of_day)
            if day:
                lessons_by_week_days[day].append(lesson)

        return WeekEntity(parsed_at=group.schedule_parsed_at, week_parity=week_parity, week_days=lessons_by_week_days)

    async def get_schedule_with_week_days_by_group_id(self, group_id: UUID, week_parity: WeekParity) -> WeekEntity:
        group = await self._group_service.get_by_id(group_id)
        return await self._get_schedule_with_week_days_by_group(group, week_parity=week_parity)

    async def get_schedule_with_week_days_by_group_name(self, group_name: str, week_parity: WeekParity) -> WeekEntity:
        group = await self._group_service.get_by_name(group_name)
        return await self._get_schedule_with_week_days_by_group(group, week_parity=week_parity)

    async def _get_schedule_with_dates_by_group(
        self,
        group: GroupEntity,
        date_from: dt.date,
        days: int
    ) -> ScheduleEntity:
        dates = [date_from + dt.timedelta(days=x) for x in range(days + 1)]
        group_lessons = await self._lesson_service.get_by_group_id(group.id)

        schedule_days = list()
        for date in dates:
            parity = WeekParity.get_parity_for_date(date)
            schedule_day = DayEntity(
                date=date,
                parity=parity,
                lessons=self._filter_lessons_by_date(group_lessons, date),
            )
            schedule_days.append(schedule_day)

        return ScheduleEntity(parsed_at=group.schedule_parsed_at, days=schedule_days)

    async def get_schedule_with_dates_by_group_id(
        self,
        group_id: UUID,
        date_from: dt.date,
        days_count: int
    ) -> ScheduleEntity:
        group = await self._group_service.get_by_id(group_id)
        return await self._get_schedule_with_dates_by_group(group, date_from, days_count)

    async def get_schedule_with_dates_by_group_name(
        self,
        group_name: str,
        date_from: dt.date,
        days_count: int
    ) -> ScheduleEntity:
        group = await self._group_service.get_by_name(group_name)
        return await self._get_schedule_with_dates_by_group(group, date_from, days_count)
