from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status

from pocket_kai.application.dto.teacher import NewTeacherDTO
from pocket_kai.application.interactors.teacher import (
    CreateTeacherInteractor,
    GetTeacherByLoginInteractor,
)
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.teacher import TeacherCreate, TeacherRead
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
    name='Получить преподавателя по логину',
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
