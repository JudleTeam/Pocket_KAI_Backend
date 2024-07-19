from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from pocket_kai.application.interactors.service_token import CheckServiceTokenInteractor
from pocket_kai.application.interactors.user import GetUserByAccessTokenInteractor
from pocket_kai.domain.entitites.user import UserEntity
from pocket_kai.domain.exceptions.auth import InvalidTokenError
from pocket_kai.domain.exceptions.user import UserError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


@inject
async def check_service_token(
    x_service_token: Annotated[str | None, Header()] = None,
    *,
    interactor: FromDishka[CheckServiceTokenInteractor],
) -> None:
    if x_service_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Service token is required',
        )

    is_token_valid = await interactor(token=x_service_token)
    if not is_token_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad service token',
        )


@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    *,
    interactor: FromDishka[GetUserByAccessTokenInteractor],
) -> UserEntity:
    try:
        return await interactor(access_token=token)
    except (InvalidTokenError, UserError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


def get_current_active_user(
    current_user: Annotated[UserEntity, Depends(get_current_user)],
) -> UserEntity:
    if current_user.is_blocked:
        raise HTTPException(status_code=401, detail='Blocked user')

    return current_user
