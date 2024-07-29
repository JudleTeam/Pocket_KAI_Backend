import asyncio
from collections import defaultdict

import logging

from utils.exam_updater_helper import (
    find_changes_in_exams,
    get_parsed_exam_key,
    get_pocket_kai_exam_key,
    get_previous_semester,
)
from utils.kai_parser_api.base import KaiParserApiBase
from utils.kai_parser_api.schemas import ParsedExam, ParsedGroup
from utils.pocket_kai_api.base import PocketKaiApiBase
from utils.pocket_kai_api.schemas import (
    PocketKaiDiscipline,
    PocketKaiExam,
    PocketKaiGroup,
    PocketKaiTeacher,
)


class ExamsUpdater:
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

        pocket_kai_group_kai_ids = {
            pocket_kai_group.kai_id for pocket_kai_group in pocket_kai_groups
        }

        return [
            parsed_group
            for parsed_group in parsed_groups
            if parsed_group.id not in pocket_kai_group_kai_ids
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

    async def update_group_exams(
        self,
        group: PocketKaiGroup,
        teachers: dict[str, PocketKaiTeacher | None],
        disciplines: dict[int, PocketKaiDiscipline | None],
    ):
        parsed_group_exams = await self.kai_parser_api.get_group_exams(
            group_kai_id=group.kai_id,
            group_name=group.group_name,
        )

        previous_academic_year, previous_academic_year_half = get_previous_semester(
            academic_year=parsed_group_exams.year_data.academic_year,
            academic_year_half=parsed_group_exams.year_data.academic_year_half,
        )
        previous_group_exams = await self.pocket_kai_api.get_exams_by_group_id(
            group_id=group.id,
            academic_year=previous_academic_year,
            academic_year_half=previous_academic_year_half,
        )

        parsed_exams_keys = [
            get_parsed_exam_key(exam) for exam in parsed_group_exams.parsed_exams
        ]
        if previous_group_exams and all(
            get_pocket_kai_exam_key(previous_exam) in parsed_exams_keys
            for previous_exam in previous_group_exams
        ):
            logging.info(
                f'Group: {group.group_name} | There are still old exams on the schedule',
            )
            return

        current_group_exams = await self.pocket_kai_api.get_exams_by_group_id(
            group_id=group.id,
            academic_year=parsed_group_exams.year_data.academic_year,
            academic_year_half=parsed_group_exams.year_data.academic_year_half,
        )

        unchanged_exams, changed_exams, exams_to_add, exams_to_delete = (
            find_changes_in_exams(
                parsed_exams=parsed_group_exams.parsed_exams,
                pocket_kai_exams=current_group_exams,
            )
        )

        logging.info(
            f'Group: {group.group_name} | {len(unchanged_exams)} unchanged exams | {len(changed_exams)} changed exams | {len(exams_to_add)} new exams | {len(exams_to_delete)} deleted exams',
        )

        for changed_exam in changed_exams:
            old_exam: PocketKaiExam = changed_exam['old']
            new_exam: ParsedExam = changed_exam['new']

            logging.info(changed_exam['differences'])

            if 'teacher_login' in changed_exam['differences']:
                teacher = await self.get_or_add_teacher(
                    teachers=teachers,
                    exam=new_exam,
                )
            else:
                teacher = old_exam.teacher

            await self.pocket_kai_api.update_exam(
                exam_id=old_exam.id,
                created_at=old_exam.created_at,
                original_date=new_exam.date,
                time=new_exam.time,
                audience_number=new_exam.audience_number,
                building_number=new_exam.building_number,
                parsed_date=new_exam.parsed_date,
                academic_year=parsed_group_exams.year_data.academic_year,
                academic_year_half=parsed_group_exams.year_data.academic_year_half,
                semester=parsed_group_exams.year_data.semester,
                discipline_id=old_exam.discipline.id,
                teacher_id=teacher.id,
                group_id=old_exam.group_id,
            )

        saved_new_exams = list()
        for exam in exams_to_add:
            teacher = await self.get_or_add_teacher(teachers, exam)
            discipline = await self.get_or_add_discipline(disciplines, exam)

            saved_new_exams.append(
                await self.pocket_kai_api.add_exam(
                    original_date=exam.date,
                    time=exam.time,
                    audience_number=exam.audience_number,
                    building_number=exam.building_number,
                    parsed_date=exam.parsed_date,
                    academic_year=parsed_group_exams.year_data.academic_year,
                    academic_year_half=parsed_group_exams.year_data.academic_year_half,
                    semester=parsed_group_exams.year_data.semester,
                    discipline_id=discipline.id,
                    teacher_id=teacher.id,
                    group_id=group.id,
                ),
            )

        for exam in exams_to_delete:
            await self.pocket_kai_api.delete_exam(exam.id)

        await self.pocket_kai_api.patch_group(
            group_id=group.id,
            schedule_parsed_at=group.schedule_parsed_at,
            exams_parsed_at=parsed_group_exams.parsed_at,
        )

        return saved_new_exams

    async def update_exams_for_groups_by_chunks(self, groups: list[PocketKaiGroup]):
        cached_teachers = defaultdict(lambda: None)
        cached_disciplines = defaultdict(lambda: None)

        chunk_size = 50
        chunks_count = len(groups) // chunk_size + 1
        logging.info(f'Groups are divided into {chunks_count} chunks')
        for chunk_num, chunk in enumerate(self.chunks(groups, chunk_size), start=1):
            tasks = [
                asyncio.create_task(
                    self.update_group_exams(
                        group=group,
                        teachers=cached_teachers,
                        disciplines=cached_disciplines,
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

    async def get_or_add_teacher(
        self,
        teachers: dict,
        exam: ParsedExam,
    ) -> PocketKaiTeacher | None:
        if not exam.teacher_login:
            return None

        if not teachers[exam.teacher_login]:
            teacher = await self.pocket_kai_api.get_teacher_by_login(
                login=exam.teacher_login,
            )
            if teacher is None:
                teacher = await self.pocket_kai_api.create_or_get_teacher_by_login(
                    login=exam.teacher_login,
                    name=exam.teacher_name,
                )
                logging.info('New teacher added')
            teachers[teacher.login] = teacher
        return teachers[exam.teacher_login]

    async def get_or_add_discipline(
        self,
        disciplines: dict[int, PocketKaiDiscipline],
        exam: ParsedExam,
    ) -> PocketKaiDiscipline:
        if not disciplines[exam.discipline_number]:
            discipline = await self.pocket_kai_api.get_discipline_by_kai_id(
                kai_id=exam.discipline_number,
            )
            if discipline is None:
                discipline = (
                    await self.pocket_kai_api.create_or_get_discipline_by_kai_id(
                        name=exam.discipline_name,
                        kai_id=exam.discipline_number,
                    )
                )
                logging.info('New discipline added')
            disciplines[discipline.kai_id] = discipline
        return disciplines[exam.discipline_number]

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    async def __call__(self):
        logging.info('Getting existing groups from PocketKAI...')
        pocket_kai_groups = await self.pocket_kai_api.get_all_groups()
        logging.info(f'Got {len(pocket_kai_groups)} groups from PocketKAI')

        new_groups = await self.find_new_groups(pocket_kai_groups)
        logging.info(f'{len(new_groups)} new groups to add')

        logging.info('Adding new groups to PocketKAI...')
        new_pocket_kai_groups = await self.add_groups(new_groups)
        logging.info('New groups added to PocketKAI!')

        all_pocket_kai_groups = pocket_kai_groups + new_pocket_kai_groups

        logging.info('Starting update exams for each group...')
        await self.update_exams_for_groups_by_chunks(all_pocket_kai_groups)
