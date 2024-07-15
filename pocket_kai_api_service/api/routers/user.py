from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import StudentUseCaseDep, get_current_active_user
from api.schemas.common import ErrorMessage
from api.schemas.student import StudentRead
from api.schemas.user import UserRead
from core.entities.user import UserEntity
from core.exceptions.base import EntityNotFoundError


router = APIRouter()


@router.get(
    '/me',
    response_model=UserRead,
)
async def get_me(
    current_user: Annotated[UserEntity, Depends(get_current_active_user)],
):
    """
    Возвращает текущего пользователя по Access-токену.
    """
    return current_user


@router.get(
    '/me/student',
    response_model=StudentRead,
    responses={
        404: {
            'description': 'Нет связанного студента',
            'model': ErrorMessage,
        },
    },
)
async def get_current_student(
    current_user: Annotated[UserEntity, Depends(get_current_active_user)],
    student_usecase: StudentUseCaseDep,
):
    """
    Возвращает студента связанного с текущим пользователем по Access-токену.
    """
    try:
        return await student_usecase.get_by_user_id(current_user.id)
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No linked KAI user found',
        )
