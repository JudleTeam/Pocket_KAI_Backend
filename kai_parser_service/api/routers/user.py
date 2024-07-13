import asyncio
import logging
from typing import Annotated

import aiohttp
from fastapi import APIRouter, Form, HTTPException, status, BackgroundTasks

from api.dependencies import KaiUserParserDep
from utils.kai_parser.user_parser import KaiUserParser


router = APIRouter()


@router.post(
    '/login',
)
async def login_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    parse_user_data: bool = True,
    *,
    kai_user_parser: KaiUserParserDep,
    background_tasks: BackgroundTasks,
):
    try:
        result = await kai_user_parser.kai_login(login=username, password=password)
    except Exception as e:
        # TODO: обновить обработку ошибок
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad credentials',
        )

    try:
        tasks = (kai_user_parser.get_user_about(), kai_user_parser.get_user_info())
        user_about, user_info = await asyncio.gather(*tasks)
    except Exception as e:
        # TODO: обновить обработку ошибок
        raise HTTPException(status_code=500, detail=str(e))

    if parse_user_data:
        background_tasks.add_task(
            parse_additional_user_data,
            login=kai_user_parser.login,
            group_name=user_about.groupNum,
            login_cookies=kai_user_parser.cookies,
        )

    return {'user_about': user_about, 'user_info': user_info}


async def parse_additional_user_data(login, group_name, login_cookies):
    async with aiohttp.ClientSession() as session:
        kai_user_parser = KaiUserParser(
            session=session,
        )

        kai_user_parser.login = login
        kai_user_parser.cookies = login_cookies

        tasks = [
            parse_user_group_members(kai_user_parser, group_name),
            parse_user_group_documents(kai_user_parser),
        ]

        await asyncio.gather(*tasks)

    logging.info('Background task done')


async def parse_user_group_members(kai_user_parser, group_name) -> bool:
    group = await kai_user_parser.get_user_group_members(group_name=str(group_name))

    logging.info(group)

    return True


async def parse_user_group_documents(kai_user_parser) -> bool:
    documents = await kai_user_parser.get_documents()

    logging.info(documents)

    return True
