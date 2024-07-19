from dishka import FromDishka
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Query, status

from pocket_kai.application.interactors.task import GetTasksInteractor
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.task import TaskRead
from pocket_kai.domain.exceptions.kai_parser import KaiParserApiError
from pocket_kai.infrastructure.kai_parser_api.schemas import TaskStatus, TaskType


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '',
    response_model=list[TaskRead],
    responses={
        503: {
            'description': 'Сервис парсинга КАИ недоступен',
            'model': ErrorMessage,
        },
    },
    name='Получить фоновые задачи',
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
    interactor: FromDishka[GetTasksInteractor],
):
    """
    Возвращает список фоновых задач с заданными параметрами.
    Сортируются по времени создания - от самой последней до самой первой.
    """
    try:
        return await interactor(
            limit=limit,
            offset=offset,
            group_name=group_name,
            login=login,
            task_type=task_type,
            task_status=task_status,
        )
    except KaiParserApiError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='KAI parser service unavailable',
        )
