import asyncio
import logging
from collections import defaultdict

from utils.schedule_updater_helper import find_changes_in_lessons
from utils.kai_parser_api.base import KaiParserApiBase
from utils.kai_parser_api.schemas import ParsedGroup, ParsedLesson
from utils.pocket_kai_api.base import PocketKaiApiBase
from utils.pocket_kai_api.schemas import (
    PocketKaiDepartment,
    PocketKaiGroup,
    PocketKaiTeacher,
)


class ScheduleUpdater:
    def __init__(
        self,
        kai_parser_api: KaiParserApiBase,
        pocket_kai_api: PocketKaiApiBase,
    ):
        self.kai_parser_api = kai_parser_api
        self.pocket_kai_api = pocket_kai_api

    async def find_new_groups(
        self,
        pocket_kai_groups: list[PocketKaiGroup],
    ) -> list[ParsedGroup]:
        logging.info('Getting group from KAI...')
        parsed_groups = await self.kai_parser_api.get_groups()
        logging.info(f'Got {len(parsed_groups)} groups from KAI')

        pocket_kai_group_ids = {
            pocket_kai_group.kai_id for pocket_kai_group in pocket_kai_groups
        }

        return [
            parsed_group
            for parsed_group in parsed_groups
            if parsed_group.id not in pocket_kai_group_ids
        ]

    async def add_groups(
        self,
        groups_to_add: list[ParsedGroup],
    ) -> list[PocketKaiGroup]:
        new_pocket_kai_groups = list()
        for group in groups_to_add:
            new_pocket_kai_groups.append(
                await self.pocket_kai_api.add_group(
                    group_name=group.name,
                    group_kai_id=group.id,
                ),
            )

        return new_pocket_kai_groups

    async def update_group_schedule(
        self,
        group: PocketKaiGroup,
        teachers: dict,
        departments: dict,
        disciplines: dict,
    ):
        parsed_group_schedule = await self.kai_parser_api.get_group_schedule(
            group.kai_id,
        )
        pocket_kai_group_lessons = (
            await self.pocket_kai_api.get_group_lessons_by_group_id(group.id)
        )

        unchanged_lessons, changed_lessons, lessons_to_add, lessons_to_delete = (
            find_changes_in_lessons(
                parsed_group_schedule.lessons,
                pocket_kai_group_lessons,
            )
        )

        logging.info(
            f'Group: {group.group_name} | {len(unchanged_lessons)} unchanged lessons |  {len(changed_lessons)} changed lessons | {len(lessons_to_add)} new lessons | {len(lessons_to_delete)} deleted lessons',
        )

        for changed_lesson in changed_lessons:
            old_lesson = changed_lesson['old']
            new_lesson = changed_lesson['new']

            logging.info(changed_lesson['differences'])

            if 'teacher_login' in changed_lesson['differences']:
                teacher = await self.get_or_add_teacher(
                    teachers,
                    new_lesson,
                )
            else:
                teacher = old_lesson.teacher

            if 'department_id' in changed_lesson['differences']:
                department = await self.get_or_add_department(departments, new_lesson)
            else:
                department = old_lesson.department

            await self.pocket_kai_api.update_group_lesson(
                lesson_id=old_lesson.id,
                created_at=old_lesson.created_at,
                number_of_day=new_lesson.day_number,
                original_dates=new_lesson.dates,
                parsed_parity=new_lesson.parsed_parity,
                parsed_dates=new_lesson.parsed_dates,
                parsed_dates_status=new_lesson.parsed_dates_status,
                audience_number=new_lesson.audience_number,
                building_number=new_lesson.building_number,
                original_lesson_type=new_lesson.discipline_type,
                parsed_lesson_type=new_lesson.parsed_lesson_type,
                start_time=new_lesson.start_time,
                end_time=new_lesson.end_time,
                discipline_id=old_lesson.discipline.id,
                teacher_id=teacher.id if teacher else None,
                department_id=department.id if department else None,
                group_id=old_lesson.group_id,
            )

        saved_new_lessons = list()
        for lesson in lessons_to_add:
            department = await self.get_or_add_department(departments, lesson)
            teacher = await self.get_or_add_teacher(teachers, lesson)
            discipline = await self.get_or_add_discipline(disciplines, lesson)

            saved_new_lessons.append(
                await self.add_group_lesson(
                    lesson,
                    group,
                    department,
                    teacher,
                    discipline,
                ),
            )

        for lesson in lessons_to_delete:
            await self.pocket_kai_api.delete_group_lesson(lesson.id)

        await self.pocket_kai_api.patch_group(
            group_id=group.id,
            schedule_parsed_at=parsed_group_schedule.parsed_at,
        )

        return saved_new_lessons

    async def update_schedule_for_groups(self, groups: list[PocketKaiGroup]):
        teachers = defaultdict(lambda: None)
        departments = defaultdict(lambda: None)
        disciplines = defaultdict(lambda: None)

        groups_count = len(groups)
        for num, group in enumerate(groups, start=1):
            logging.info(
                f'[{num}/{groups_count}] Working with group {group.group_name}...',
            )

            try:
                await self.update_group_schedule(
                    group,
                    teachers,
                    departments,
                    disciplines,
                )
            except Exception as e:
                logging.error(f'Error with group {group.group_name}: {e}')

            logging.info(f'Schedule updating for group {group.group_name} done!')

    async def update_schedule_for_groups_by_chunks(self, groups: list[PocketKaiGroup]):
        teachers = defaultdict(lambda: None)
        departments = defaultdict(lambda: None)
        disciplines = defaultdict(lambda: None)

        chunk_size = 50
        chunks_count = len(groups) // chunk_size + 1
        logging.info(f'Groups are divided into {chunks_count} chunks')
        for chunk_num, chunk in enumerate(self.chunks(groups, chunk_size), start=1):
            tasks = [
                asyncio.create_task(
                    self.update_group_schedule(
                        group,
                        teachers,
                        departments,
                        disciplines,
                    ),
                )
                for group in chunk
            ]
            for task in asyncio.as_completed(tasks):
                try:
                    await task
                except Exception as e:
                    logging.error(f'Error with some group: {e}')

            logging.info(f'Chunk {chunk_num}/{chunks_count} done')

    async def get_or_add_department(
        self,
        departments: dict,
        lesson: ParsedLesson,
    ) -> PocketKaiDepartment | None:
        if lesson.department_id is None:
            return None

        if not departments[lesson.department_id]:
            department = await self.pocket_kai_api.get_department_by_kai_id(
                lesson.department_id,
            )
            if department is None:
                department = (
                    await self.pocket_kai_api.create_or_get_department_by_kai_id(
                        name=lesson.department_name,
                        kai_id=lesson.department_id,
                    )
                )
                logging.info('New department added')
            departments[department.kai_id] = department
            return department

        return departments[lesson.department_id]

    async def get_or_add_teacher(
        self,
        teachers: dict,
        lesson: ParsedLesson,
    ) -> PocketKaiTeacher | None:
        if not lesson.teacher_login:
            return None

        if not teachers[lesson.teacher_login]:
            teacher = await self.pocket_kai_api.get_teacher_by_login(
                lesson.teacher_login,
            )
            if teacher is None:
                teacher = await self.pocket_kai_api.create_or_get_teacher_by_login(
                    login=lesson.teacher_login,
                    name=lesson.teacher_name,
                )
                logging.info('New teacher added')
            teachers[teacher.login] = teacher
        return teachers[lesson.teacher_login]

    async def get_or_add_discipline(self, disciplines, lesson):
        if not disciplines[lesson.discipline_number]:
            discipline = await self.pocket_kai_api.get_discipline_by_kai_id(
                lesson.discipline_number,
            )
            if discipline is None:
                discipline = (
                    await self.pocket_kai_api.create_or_get_discipline_by_kai_id(
                        name=lesson.discipline_name,
                        kai_id=lesson.discipline_number,
                    )
                )
                logging.info('New discipline added')
            disciplines[discipline.kai_id] = discipline
        return disciplines[lesson.discipline_number]

    async def add_group_lesson(
        self,
        lesson: ParsedLesson,
        group,
        department,
        teacher: PocketKaiTeacher | None,
        discipline,
    ):
        return await self.pocket_kai_api.add_group_lesson(
            number_of_day=lesson.day_number,
            original_dates=lesson.dates,
            parsed_parity=lesson.parsed_parity,
            parsed_dates=lesson.parsed_dates,
            parsed_dates_status=lesson.parsed_dates_status,
            audience_number=lesson.audience_number,
            building_number=lesson.building_number,
            original_lesson_type=lesson.discipline_type,
            parsed_lesson_type=lesson.parsed_lesson_type,
            start_time=lesson.start_time,
            end_time=lesson.end_time,
            discipline_id=discipline.id,
            teacher_id=teacher.id if teacher else None,
            department_id=department.id if department else None,
            group_id=group.id,
        )

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    async def __call__(self, split_to_chunks: bool = False, *args, **kwargs):
        logging.info('Getting existing groups from PocketKAI...')
        pocket_kai_groups = await self.pocket_kai_api.get_all_groups()
        logging.info(f'Got {len(pocket_kai_groups)} groups from PocketKAI')

        new_groups = await self.find_new_groups(pocket_kai_groups)
        logging.info(f'{len(new_groups)} new groups to add')

        logging.info('Adding new groups to PocketKAI...')
        new_pocket_kai_groups = await self.add_groups(new_groups)
        logging.info('New groups added to PocketKAI!')

        all_pocket_kai_groups = pocket_kai_groups + new_pocket_kai_groups

        logging.info('Starting update schedule for each group...')
        if split_to_chunks:
            await self.update_schedule_for_groups_by_chunks(all_pocket_kai_groups)
        else:
            await self.update_schedule_for_groups(all_pocket_kai_groups)
