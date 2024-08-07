from uuid import UUID

from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, Query, status

from pocket_kai.application.dto.teacher import NewTeacherDTO
from pocket_kai.application.interactors.lesson import GetLessonsByTeacherIdInteractor
from pocket_kai.application.interactors.teacher import (
    CreateTeacherInteractor,
    GetTeacherByLoginInteractor,
    SuggestTeachersByNameInteractor,
)
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.lesson import TeacherLessonRead
from pocket_kai.controllers.schemas.teacher import TeacherCreate, TeacherRead
from pocket_kai.domain.common import WeekParity
from pocket_kai.domain.exceptions.teacher import (
    TeacherAlreadyExistsError,
    TeacherNotFoundError,
)


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '/by_login/{login}',
    response_model=TeacherRead,
    responses={
        404: {
            'description': 'Преподаватель не найден',
            'model': ErrorMessage,
        },
    },
)
async def get_teacher_by_login(
    login: str,
    *,
    interactor: FromDishka[GetTeacherByLoginInteractor],
):
    """
    Возвращает преподавателя по его логину с сайта КАИ.
    *Берётся из базы данных Pocket KAI, а не сайта КАИ!*
    """
    try:
        return await interactor(login=login)
    except TeacherNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Teacher with login "{login}" not found',
        )


@router.get(
    '/by_id/{teacher_id}/schedule',
    response_model=list[TeacherLessonRead],
    responses={
        404: {
            'description': 'Преподаватель не найден',
            'model': ErrorMessage,
        },
    },
)
async def get_teacher_schedule(
    teacher_id: UUID,
    week_parity: WeekParity = WeekParity.ANY,
    *,
    interactor: FromDishka[GetLessonsByTeacherIdInteractor],
):
    """
    Возвращает расписание преподавателя по его ID.
    Если занятия дублируются для нескольких групп, то
    """
    try:
        return await interactor(teacher_id=str(teacher_id), week_parity=week_parity)
    except TeacherNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Teacher with id "{teacher_id}" not found',
        )


@router.get(
    '/suggest_by_name',
    response_model=list[TeacherRead],
)
async def suggest_teachers_by_name(
    name: str,
    limit: Annotated[int, Query(gt=0, le=50)] = 20,
    *,
    interactor: FromDishka[SuggestTeachersByNameInteractor],
):
    """
    Предлагает преподавателей по части ФИО.
    Допускаются опечатки или небольшие неточности в запросе.
    """
    return await interactor(name=name, limit=limit)


@router.post(
    '',
    response_model=TeacherRead,
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def create_teacher(
    teacher_create: TeacherCreate,
    *,
    interactor: FromDishka[CreateTeacherInteractor],
):
    try:
        return await interactor(
            NewTeacherDTO(
                login=teacher_create.login,
                name=teacher_create.name,
            ),
        )
    except TeacherAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Teacher with provided login already exists',
        )
