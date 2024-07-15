from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import check_service_token, TeacherServiceDep
from api.schemas.common import ErrorMessage
from api.schemas.teacher import TeacherCreate, TeacherRead
from core.exceptions.base import (
    EntityAlreadyExistsError,
    BadRelatedEntityError,
    EntityNotFoundError,
)


router = APIRouter()


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
    teacher_service: TeacherServiceDep,
):
    """
    Возвращает преподавателя по его логину с сайта КАИ.
    *Берётся из базы данных Pocket KAI, а не сайта КАИ!*
    """
    try:
        return await teacher_service.get_by_login(login=login)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post(
    '',
    response_model=TeacherRead,
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def create_teacher(
    teacher_create: TeacherCreate,
    teacher_service: TeacherServiceDep,
):
    try:
        return await teacher_service.create(teacher_create)
    except EntityAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Teacher with provided login already exists',
        )
    except BadRelatedEntityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad department ID',
        )
