from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from api.dependencies import TaskUseCaseDep
from api.schemas.common import ErrorMessage
from api.schemas.task import TaskRead
from core.exceptions.kai_parser import KaiParserApiError
from utils.kai_parser_api.schemas import TaskStatus, TaskType


router = APIRouter()


@router.get(
    '',
    response_model=list[TaskRead],
    responses={
        503: {
            'description': 'Сервис парсинга КАИ недоступен',
            'model': ErrorMessage,
        },
    },
)
async def get_tasks(
    limit: int = 10,
    offset: int = 0,
    group_name: Annotated[
        str | None,
        Query(title='Номер группы', description='Номер группы для поиска задач'),
    ] = None,
    login: Annotated[
        str | None,
        Query(title='Логин студента', description='Логин студента для поиска задач'),
    ] = None,
    task_type: Annotated[
        TaskType | None,
        Query(title='Тип задачи', description='Тип задачи для поиска'),
    ] = None,
    task_status: Annotated[
        TaskStatus | None,
        Query(title='Статус задачи', description='Статус задачи для поиска'),
    ] = None,
    *,
    task_usecase: TaskUseCaseDep,
):
    """
    Возвращает список фоновых задач с заданными параметрами.
    Сортируются по времени создания - от самой последней до самой первой.
    """
    try:
        return await task_usecase.get_tasks(
            limit=limit,
            offset=offset,
            group_name=group_name,
            login=login,
            type=task_type,
            status=task_status,
        )
    except KaiParserApiError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='KAI parser service unavailable',
        )