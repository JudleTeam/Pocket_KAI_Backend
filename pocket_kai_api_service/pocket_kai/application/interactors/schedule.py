import datetime as dt


from pocket_kai.application.dto.lesson import LessonExtendedDTO
from pocket_kai.application.dto.schedule import (
    DayDTO,
    ScheduleDTO,
    WeekDTO,
    WeekDaysDTO,
)
from pocket_kai.application.interactors.lesson import ExtendedLessonConverter
from pocket_kai.application.interfaces.entities.group import GroupReader
from pocket_kai.application.interfaces.entities.lesson import LessonReader
from pocket_kai.domain.common import WeekParity
from pocket_kai.domain.entitites.group import GroupEntity
from pocket_kai.domain.entitites.lesson import LessonEntity
from pocket_kai.domain.exceptions.group import GroupNotFoundError


async def week_schedule(
    group_lessons: list[LessonEntity],
    group: GroupEntity,
    week_parity: WeekParity,
    lesson_extended_converter: ExtendedLessonConverter,
) -> WeekDaysDTO:
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
            lessons_by_week_days[day].append(await lesson_extended_converter(lesson))

    return WeekDaysDTO(
        parsed_at=group.schedule_parsed_at,
        week_parity=week_parity,
        week_days=WeekDTO(
            monday=lessons_by_week_days['monday'],
            tuesday=lessons_by_week_days['tuesday'],
            wednesday=lessons_by_week_days['wednesday'],
            thursday=lessons_by_week_days['thursday'],
            friday=lessons_by_week_days['friday'],
            saturday=lessons_by_week_days['saturday'],
            sunday=lessons_by_week_days['sunday'],
        ),
    )


class GetWeekScheduleByGroupNameInteractor:
    def __init__(
        self,
        lesson_gateway: LessonReader,
        group_gateway: GroupReader,
        lesson_extended_converter: ExtendedLessonConverter,
    ):
        self._lesson_gateway = lesson_gateway
        self._group_gateway = group_gateway
        self._lesson_extended_converter = lesson_extended_converter

    async def __call__(self, group_name: str, week_parity: WeekParity) -> WeekDaysDTO:
        group = await self._group_gateway.get_by_name(group_name)
        if group is None:
            raise GroupNotFoundError

        group_lessons = await self._lesson_gateway.get_by_group_id(
            group_id=group.id,
            week_parity=week_parity,
        )

        return await week_schedule(
            group_lessons=group_lessons,
            group=group,
            week_parity=week_parity,
            lesson_extended_converter=self._lesson_extended_converter,
        )


class GetWeekScheduleByGroupIdInteractor:
    def __init__(
        self,
        lesson_gateway: LessonReader,
        group_gateway: GroupReader,
        lesson_extended_converter: ExtendedLessonConverter,
    ):
        self._lesson_gateway = lesson_gateway
        self._group_gateway = group_gateway
        self._lesson_extended_converter = lesson_extended_converter

    async def __call__(self, group_id: str, week_parity: WeekParity) -> WeekDaysDTO:
        group = await self._group_gateway.get_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        group_lessons = await self._lesson_gateway.get_by_group_id(
            group_id=group.id,
            week_parity=week_parity,
        )

        return await week_schedule(
            group_lessons=group_lessons,
            group=group,
            week_parity=week_parity,
            lesson_extended_converter=self._lesson_extended_converter,
        )


def _filter_lessons_by_date(
    group_lessons: list[LessonExtendedDTO],
    date: dt.date,
) -> list[LessonExtendedDTO]:
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


async def form_schedule(
    date_from: dt.date,
    days_count: int,
    group_lessons: list[LessonExtendedDTO],
    group: GroupEntity,
):
    dates = [date_from + dt.timedelta(days=x) for x in range(days_count)]

    schedule_days = list()
    for date in dates:
        parity = WeekParity.get_parity_for_date(date)
        schedule_day = DayDTO(
            date=date,
            parity=parity,
            lessons=_filter_lessons_by_date(group_lessons, date),
        )
        schedule_days.append(schedule_day)

    return ScheduleDTO(parsed_at=group.schedule_parsed_at, days=schedule_days)


class GetDatesScheduleByGroupNameInteractor:
    def __init__(
        self,
        lesson_gateway: LessonReader,
        group_gateway: GroupReader,
        lesson_extended_converter: ExtendedLessonConverter,
    ):
        self._lesson_gateway = lesson_gateway
        self._group_gateway = group_gateway
        self._lesson_extended_converter = lesson_extended_converter

    async def __call__(
        self,
        group_name: str,
        date_from: dt.date,
        days_count: int,
    ) -> ScheduleDTO:
        group = await self._group_gateway.get_by_name(group_name)
        if group is None:
            raise GroupNotFoundError

        group_lessons = await self._lesson_gateway.get_by_group_id_extended(
            group.id,
            week_parity=WeekParity.ANY,
        )

        return await form_schedule(
            date_from=date_from,
            days_count=days_count,
            group_lessons=group_lessons,
            group=group,
        )


class GetDatesScheduleByGroupIdInteractor:
    def __init__(
        self,
        lesson_gateway: LessonReader,
        group_gateway: GroupReader,
        lesson_extended_converter: ExtendedLessonConverter,
    ):
        self._lesson_gateway = lesson_gateway
        self._group_gateway = group_gateway
        self._lesson_extended_converter = lesson_extended_converter

    async def __call__(
        self,
        group_id: str,
        date_from: dt.date,
        days_count: int,
    ) -> ScheduleDTO:
        group = await self._group_gateway.get_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        group_lessons = await self._lesson_gateway.get_by_group_id_extended(
            group.id,
            week_parity=WeekParity.ANY,
        )

        return await form_schedule(
            date_from=date_from,
            days_count=days_count,
            group_lessons=group_lessons,
            group=group,
        )
