from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status, BackgroundTasks

from api.dependencies import KaiUserParserDep
from core.exceptions.api import KaiApiError
from utils.tasks.additional_user_data import parse_additional_user_data


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
    except KaiApiError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Error during KAI parsing',
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad credentials',
        )

    try:
        user_info = await kai_user_parser.get_user_info()
        user_about = await kai_user_parser.get_user_about()
    except KaiApiError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Error during KAI parsing',
        )

    if parse_user_data:
        background_tasks.add_task(
            parse_additional_user_data,
            login=kai_user_parser.login,
            group_name=user_about.groupNum,
            login_cookies=kai_user_parser.cookies,
        )

    return {'user_about': user_about, 'user_info': user_info}
