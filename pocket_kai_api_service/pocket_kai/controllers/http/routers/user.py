from dishka.integrations.fastapi import DishkaRoute
from typing import Annotated

from dishka import FromDishka
from fastapi import APIRouter, Depends, HTTPException, status

from pocket_kai.application.interactors.student import (
    GetGroupMembersByUserIdInteractor,
    GetStudentByUserIdInteractor,
)
from pocket_kai.controllers.http.dependencies import get_current_active_user
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.student import GroupMemberRead, StudentRead
from pocket_kai.controllers.schemas.user import UserRead
from pocket_kai.domain.entitites.user import UserEntity
from pocket_kai.domain.exceptions.student import StudentNotFoundError


router = APIRouter(route_class=DishkaRoute)


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
    *,
    interactor: FromDishka[GetStudentByUserIdInteractor],
):
    """
    Возвращает студента связанного с текущим пользователем по Access-токену.
    """
    try:
        return await interactor(user_id=current_user.id)
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No linked KAI user found',
        )


@router.get(
    '/me/student/group_members',
    response_model=list[GroupMemberRead],
)
async def get_group_members_for_current_student(
    current_user: Annotated[UserEntity, Depends(get_current_active_user)],
    *,
    interactor: FromDishka[GetGroupMembersByUserIdInteractor],
):
    """
    Возвращает список одногруппников студента (включая самого студента) связанного с текущим пользователем по Access-токену.
    """
    try:
        return await interactor(user_id=current_user.id)
    except StudentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No linked KAI user found',
        )
