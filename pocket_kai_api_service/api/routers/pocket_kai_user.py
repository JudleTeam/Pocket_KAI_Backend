from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import KaiUserServiceDep, get_current_active_user
from api.schemas.kai_user import KaiUserRead
from api.schemas.pocket_kai_user import PocketKaiUserRead
from core.entities.pocket_kai_user import PocketKaiUserEntity
from core.exceptions.base import EntityNotFoundError


router = APIRouter()


@router.get(
    '/me',
    response_model=PocketKaiUserRead,
)
async def get_me(
    current_user: Annotated[PocketKaiUserEntity, Depends(get_current_active_user)],
):
    return current_user


@router.get(
    '/me/kai_user',
    response_model=KaiUserRead,
)
async def get_current_kai_user(
    current_user: Annotated[PocketKaiUserEntity, Depends(get_current_active_user)],
    kai_user_service: KaiUserServiceDep,
):
    try:
        return await kai_user_service.get_by_pocket_kai_user_id(current_user.id)
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No linked KAI user found',
        )
