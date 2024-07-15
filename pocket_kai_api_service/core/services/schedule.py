import datetime as dt
from abc import ABC, abstractmethod
from uuid import UUID

from api.schemas.schedule import DayResponse, ScheduleResponse, WeekDaysResponse
from core.entities.group import GroupEntity
from core.entities.lesson import LessonEntity
from core.entities.common import WeekParity
from core.repositories.group import GroupRepositoryBase
from core.repositories.lesson import LessonRepositoryBase


class ScheduleServiceBase(ABC):
    def __init__(
        self,
        lesson_repository: LessonRepositoryBase,
        group_repository: GroupRepositoryBase,
    ):
        self.lesson_repository = lesson_repository
        self.group_repository = group_repository

    @abstractmethod
    async def get_schedule_with_dates_by_group_id(
        self,
        group_id: UUID,
        date_from: dt.date,
        days_count: int,
    ) -> list[DayResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_schedule_with_dates_by_group_name(
        self,
        group_name: str,
        date_from: dt.date,
        days_count: int,
    ) -> list[DayResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_week_schedule_by_group_id(
        self,
        group_id: UUID,
        week_parity: WeekParity,
    ) -> WeekDaysResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_week_schedule_by_group_name(
        self,
        group_name: str,
        week_parity: WeekParity,
    ) -> WeekDaysResponse:
        raise NotImplementedError


class ScheduleService(ScheduleServiceBase):
    @staticmethod
    def _filter_lessons_by_date(
        group_lessons: list[LessonEntity],
        date: dt.date,
    ) -> list[LessonEntity]:
        day_number = date.isoweekday()
        date_week_parity = WeekParity.get_parity_for_date(date)
        filtered_lessons = []

        for lesson in group_lessons:
            if lesson.parsed_dates:
                if date in lesson.parsed_dates:
                    filtered_lessons.append(lesson)
            elif lesson.number_of_day == day_number and lesson.parsed_parity in (
                WeekParity.ANY,
                date_week_parity,
            ):
                filtered_lessons.append(lesson)

        return filtered_lessons

    async def _get_schedule_with_week_days_by_group(
        self,
        group: GroupEntity,
        week_parity: WeekParity,
    ) -> WeekDaysResponse:
        group_lessons = await self.lesson_repository.get_by_group_id(
            group.id,
            week_parity=week_parity,
        )

        lessons_by_week_days = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': [],
        }

        day_mapping = {
            1: 'monday',
            2: 'tuesday',
            3: 'wednesday',
            4: 'thursday',
            5: 'friday',
            6: 'saturday',
            7: 'sunday',
        }

        for lesson in group_lessons:
            day = day_mapping.get(lesson.number_of_day)
            if day:
                lessons_by_week_days[day].append(lesson)

        return WeekDaysResponse(
            parsed_at=group.schedule_parsed_at,
            week_parity=week_parity,
            week_days=lessons_by_week_days,
        )

    async def get_week_schedule_by_group_id(
        self,
        group_id: UUID,
        week_parity: WeekParity,
    ) -> WeekDaysResponse:
        group = await self.group_repository.get_by_id(group_id)
        return await self._get_schedule_with_week_days_by_group(
            group,
            week_parity=week_parity,
        )

    async def get_week_schedule_by_group_name(
        self,
        group_name: str,
        week_parity: WeekParity,
    ) -> WeekDaysResponse:
        group = await self.group_repository.get_by_name(group_name)
        return await self._get_schedule_with_week_days_by_group(
            group,
            week_parity=week_parity,
        )

    async def _get_schedule_with_dates_by_group(
        self,
        group: GroupEntity,
        date_from: dt.date,
        days: int,
    ) -> ScheduleResponse:
        dates = [date_from + dt.timedelta(days=x) for x in range(days)]
        group_lessons = await self.lesson_repository.get_by_group_id(group.id)

        schedule_days = list()
        for date in dates:
            parity = WeekParity.get_parity_for_date(date)
            schedule_day = DayResponse(
                date=date,
                parity=parity,
                lessons=self._filter_lessons_by_date(group_lessons, date),
            )
            schedule_days.append(schedule_day)

        return ScheduleResponse(parsed_at=group.schedule_parsed_at, days=schedule_days)

    async def get_schedule_with_dates_by_group_id(
        self,
        group_id: UUID,
        date_from: dt.date,
        days_count: int,
    ) -> ScheduleResponse:
        group = await self.group_repository.get_by_id(group_id)
        return await self._get_schedule_with_dates_by_group(
            group,
            date_from,
            days_count,
        )

    async def get_schedule_with_dates_by_group_name(
        self,
        group_name: str,
        date_from: dt.date,
        days_count: int,
    ) -> ScheduleResponse:
        group = await self.group_repository.get_by_name(group_name)
        return await self._get_schedule_with_dates_by_group(
            group,
            date_from,
            days_count,
        )
