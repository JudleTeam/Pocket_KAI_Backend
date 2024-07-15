import logging
from datetime import datetime

from aiohttp import ClientSession

from config import get_settings
from core.common import TaskStatus, TaskType
from core.repositories.providers import get_task_repository
from core.services.providers import get_task_service
from core.unit_of_work import get_uow
from database.db import AsyncSessionmaker
from utils.kai_parser.user_parser import KaiUserParser
from utils.pocket_kai_api.api import PocketKaiApi


async def parse_additional_user_data(login, group_name, login_cookies):
    logging.info('Starting background tasks...')
    settings = get_settings()
    async with (
        ClientSession() as kai_parser_session,
        AsyncSessionmaker() as db_session,
        ClientSession() as pocket_kai_session,
    ):
        task_service = get_task_service(
            task_repository=get_task_repository(session=db_session),
            uow=get_uow(session=db_session),
        )

        kai_user_parser = KaiUserParser(session=kai_parser_session)
        kai_user_parser.login = login
        kai_user_parser.cookies = login_cookies

        pocket_kai_api = PocketKaiApi(
            base_url=settings.POCKET_KAI_BASE_URL,
            service_token=settings.SERVICE_TOKEN,
            session=pocket_kai_session,
        )

        parse_documents_task = await task_service.create(
            name=f'Parse documents for group {group_name}',
            type=TaskType.GROUP_DOCUMENTS,
            status=TaskStatus.IN_PROGRESS,
            login=login,
            group_name=str(group_name),
        )

        parse_group_members_task = await task_service.create(
            name=f'Parse group members for group {group_name}',
            type=TaskType.GROUP_MEMBERS,
            status=TaskStatus.IN_PROGRESS,
            login=login,
            group_name=str(group_name),
        )

        tasks = {
            parse_user_group_members(
                kai_user_parser,
                group_name,
                pocket_kai_api,
            ): parse_group_members_task,
            parse_user_group_documents(
                kai_user_parser,
                group_name,
                pocket_kai_api,
            ): parse_documents_task,
        }

        for task in tasks:
            task_record = tasks[task]
            try:
                await task
            except Exception as e:
                task_record.status = TaskStatus.FAILED
                task_record.errors = repr(e)
                task_record.ended_at = datetime.utcnow()
                await task_service.update(task_record)
                logging.error(f'Error with task {task_record.name}: {e}')
            else:
                task_record.status = TaskStatus.COMPLETED
                task_record.ended_at = datetime.utcnow()
                await task_service.update(task_record)
            finally:
                logging.info(f'Task {task_record.name} done')

    logging.info('Background tasks done')


async def parse_user_group_members(kai_user_parser, group_name, pocket_kai_api) -> bool:
    group_members = await kai_user_parser.get_user_group_members(
        group_name=str(group_name),
    )

    await pocket_kai_api.add_group_members(
        group_name=str(group_name),
        group_members=group_members,
    )

    return True


async def parse_user_group_documents(
    kai_user_parser,
    group_name,
    pocket_kai_api,
) -> bool:
    documents = await kai_user_parser.get_documents()

    await pocket_kai_api.patch_group(
        group_name=str(group_name),
        patch={
            'syllabus_url': documents.syllabus,
            'educational_program_url': documents.educational_program,
            'study_schedule_url': documents.study_schedule,
        },
    )

    return True
