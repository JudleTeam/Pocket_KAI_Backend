import asyncio
import datetime
import logging
from asyncio import create_task
from pprint import pprint

import tqdm.asyncio
from sqlalchemy.exc import IntegrityError

from database.base import async_session_maker
from database.models.kai import Group, GroupLesson, Teacher, Departament, Discipline
from utils.kai_parser import KaiParser
from utils.kai_parser.schemas import GroupsResult, Lesson


def parse_parity(parity: str) -> int:
    """
    0 - any week
    1 - odd week
    2 - even week
    """

    odd = False
    even = False

    # 'нея' - typo. Check misc/possible_parity.txt
    if 'нечет' in parity or 'неч' in parity or 'нея' in parity:
        odd = True
        parity = parity.replace('нечет', '')

    if 'чет' in parity:
        even = True

    if odd and not even:
        return 1
    if even and not odd:
        return 2

    return 0


def get_lesson_end_time(start_time: datetime.time, lesson_type: str) -> datetime.time | None:
    """
    Время пар не подходит для филиалов. На момент 2023-2024 учебного года на сайте КАИ есть расписание только некоторых
    филиалов, например группы с номером из 5 цифр или начинающиеся с "8" относятся к каким-то филиалам

    (Возможно стоит сделать адаптивное определение времени - получить всё возможное время начала пары для группы или
    факультета и на его основе определять время конца пары, т.е. просто собирать отдельно список start_times.
    А возможно и не стоит думать о других филиалах вообще)
    """
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

    start_time = datetime.timedelta(hours=start_time.hour, minutes=start_time.minute)

    if start_time not in start_times:
        return None

    lesson_timedelta = datetime.timedelta(hours=1, minutes=30)

    """ В этом семестре лабы разделены на 2 пары, по полтора часа """
    # if lesson_type == 'л.р.':
    #     next_lesson_ind = start_times.index(start_time) + 1
    #     if next_lesson_ind > len(start_times) - 1:
    #         # Бывают лабораторные работы в 20:00, видимо они длятся одну пару
    #         next_lesson_ind = len(start_times) - 1
    #     end_time = start_times[next_lesson_ind] + lesson_timedelta
    # else:
    #     end_time = start_time + lesson_timedelta

    end_time = start_time + lesson_timedelta

    return (datetime.datetime.min + end_time).time()


async def add_groups(groups: list[GroupsResult]) -> list[Group]:
    async with async_session_maker() as session:
        db_groups = [Group(kai_id=group.id, group_name=int(group.group)) for group in groups]
        session.add_all(db_groups)
        await session.commit()

    return db_groups


async def add_group_schedule(group_id, schedule: list[Lesson]):
    async with async_session_maker() as session:
        for lesson in schedule:
            new_department, _ = await Departament.get_or_create(
                session=session,
                commit=False,
                kai_id=lesson.orgUnitId,
                defaults={
                    'name': lesson.orgUnitName
                }
            )

            if lesson.prepodLogin:
                new_teacher, _ = await Teacher.get_or_create(
                    session=session,
                    commit=False,
                    login=lesson.prepodLogin,
                    defaults={
                        'name': lesson.prepodName,
                        'departament': new_department,
                    }
                )
            else:
                new_teacher = None

            new_discipline, _ = await Discipline.get_or_create(
                session=session,
                commit=False,
                kai_id=lesson.disciplNum,
                defaults={
                    'name': lesson.disciplName
                }
            )

            new_lesson = GroupLesson(
                number_of_day=lesson.dayNum,
                parity_of_week=lesson.dayDate,
                int_parity_of_week=parse_parity(lesson.dayDate),
                auditory_number=lesson.audNum,
                building_number=lesson.buildNum,
                lesson_type=lesson.disciplType,
                start_time=lesson.dayTime,
                end_time=get_lesson_end_time(lesson.dayTime, lesson.disciplType),
                group_id=group_id,
                teacher=new_teacher,
                discipline=new_discipline
            )
            session.add(new_lesson)
            await session.commit()


async def test(group: Group):
    schedule = await KaiParser.get_group_schedule(group.kai_id)
    await add_group_schedule(group.id, schedule)


async def parse_schedule():
    all_groups = await KaiParser.get_group_ids()

    db_groups = await add_groups(all_groups)

    tasks = [KaiParser.get_group_schedule(group.kai_id) for group in db_groups]

    all_groups_schedule = await tqdm.asyncio.tqdm.gather(*tasks, total=len(tasks))

    for group, schedule in tqdm.tqdm(zip(db_groups, all_groups_schedule), total=len(all_groups_schedule)):
        await add_group_schedule(group.id, schedule)


async def main():
    # pprint(await KaiParser.get_group_ids())
    await parse_schedule()


if __name__ == '__main__':
    asyncio.run(main())
