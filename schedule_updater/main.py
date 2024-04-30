import asyncio
import logging

from database.base import async_session_maker
from database.models.kai import Group, GroupLesson, Teacher, Department, Discipline
from utils.kai_parser import KaiParser
from utils.kai_parser.schemas import ParsedGroup, ParsedLesson


async def add_groups(groups: list[ParsedGroup]) -> list[Group]:
    db_groups = []
    async with async_session_maker() as session:
        for group in groups:
            new_group, _ = await Group.get_or_create(
                session=session,
                commit=True,
                kai_id=group.id,
                group_name=group.name
            )
            db_groups.append(new_group)

    return db_groups


async def add_group_schedule(group_id, schedule: list[ParsedLesson]):
    async with async_session_maker() as session:
        for lesson in schedule:
            new_department, _ = await Department.get_or_create(
                session=session,
                commit=False,
                kai_id=lesson.department_id,
                defaults={
                    'name': lesson.department_name
                }
            )

            if lesson.teacher_login:
                new_teacher, _ = await Teacher.get_or_create(
                    session=session,
                    commit=False,
                    login=lesson.teacher_login,
                    defaults={
                        'name': lesson.teacher_name,
                        'department': new_department,
                    }
                )
            else:
                new_teacher = None

            new_discipline, _ = await Discipline.get_or_create(
                session=session,
                commit=False,
                kai_id=lesson.discipline_number,
                defaults={
                    'name': lesson.discipline_name
                }
            )

            new_lesson = GroupLesson(
                number_of_day=lesson.day_number,
                original_dates=lesson.dates,
                parsed_parity=lesson.parsed_parity,
                parsed_dates=None,  # Future feature
                audience_number=lesson.audience_number,
                building_number=lesson.building_number,
                original_lesson_type=lesson.discipline_type,
                parsed_lesson_type=lesson.parsed_lesson_type,
                start_time=lesson.start_time,
                end_time=lesson.end_time,
                group_id=group_id,
                teacher=new_teacher,
                discipline=new_discipline
            )
            session.add(new_lesson)
            await session.commit()


async def parse_groups_schedule_sync(groups: list[Group]) -> list[list[ParsedLesson] | BaseException]:
    all_groups_schedule = []
    for group in groups:
        try:
            schedule = await KaiParser.get_group_schedule(group.kai_id)
        except Exception as e:
            all_groups_schedule.append(e)
        else:
            all_groups_schedule.append(schedule)

    return all_groups_schedule


async def parse_groups_schedule_async(groups: list[Group]) -> tuple[list[ParsedLesson] | BaseException]:
    tasks = [KaiParser.get_group_schedule(group.kai_id) for group in groups]
    return await asyncio.gather(*tasks, return_exceptions=True)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def parse_groups_schedule_async_by_chunks(
    groups: list[Group],
    chunk_size: int = 50
) -> tuple[list[ParsedLesson] | BaseException]:
    all_groups_schedule = list()
    logging.info(f'Groups are divided into {len(groups) // chunk_size + 1} chunks')
    for chunk_num, chunk in enumerate(chunks(groups, chunk_size), start=1):
        tasks = [KaiParser.get_group_schedule(group.kai_id) for group in chunk]
        all_groups_schedule += await asyncio.gather(*tasks, return_exceptions=True)
        logging.info(f'Chunk {chunk_num} done')
    return all_groups_schedule


async def parse_and_save_all_groups_schedule():
    """
    !!!Clear old group lessons before parsing new!!!
    """
    logging.basicConfig(level=logging.INFO)

    logging.info('Parsing groups...')
    all_groups = await KaiParser.get_group_ids()
    logging.info(f'Groups parsed. Total: {len(all_groups)}')

    logging.info('Saving groups...')
    db_groups = await add_groups(all_groups)
    logging.info('Groups saved.')

    logging.info('Parsing schedule')
    all_groups_schedule = await parse_groups_schedule_async_by_chunks(db_groups, chunk_size=100)
    logging.info('Schedule parsed.')

    logging.info('Saving schedule...')
    for group, schedule in zip(db_groups, all_groups_schedule):
        if isinstance(schedule, Exception):
            logging.error(f'Something wrong with group {group.group_name}: {schedule}')
            continue
        await add_group_schedule(group.id, schedule)
    logging.info('Schedule saved.')

    logging.info('All done!')


async def main():
    # pprint(await KaiParser.get_group_ids())
    await parse_and_save_all_groups_schedule()


if __name__ == '__main__':
    asyncio.run(main())
