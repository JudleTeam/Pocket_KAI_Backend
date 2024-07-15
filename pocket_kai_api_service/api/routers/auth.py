from typing import Annotated

from fastapi import APIRouter, Cookie, Form, HTTPException, Response, status

from api.dependencies import AuthUseCaseDep
from core.exceptions.auth import InvalidTokenError
from core.exceptions.base import EntityNotFoundError
from core.exceptions.kai_parser import (
    BadKaiCredentialsError,
    KaiParserApiError,
    KaiParsingError,
)


router = APIRouter()


@router.post(
    '/login',
)
async def login_with_kai_credentials(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    auth_usecase: AuthUseCaseDep,
    response: Response,
):
    try:
        access_token, refresh_token = await auth_usecase.login_by_kai(
            username=login,
            password=password,
        )
    except BadKaiCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad KAI credentials',
        )
    except KaiParsingError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Problems with parsing KAI',
        )
    except KaiParserApiError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='KAI parser service unavailable',
        )

    response.set_cookie(
        key='RefreshToken',
        value=refresh_token,
        httponly=True,
        secure=True,
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post(
    '/refresh_token',
)
async def refresh_token_pair(
    refresh_token: Annotated[str, Cookie(alias='RefreshToken')],
    auth_usecase: AuthUseCaseDep,
    response: Response,
):
    try:
        access_token, refresh_token = await auth_usecase.refresh_token_pair(
            refresh_token=refresh_token,
        )
    except (EntityNotFoundError, InvalidTokenError):
        raise HTTPException(status_code=400, detail='Invalid refresh token')

    response.set_cookie(
        key='RefreshToken',
        value=refresh_token,
        httponly=True,
        secure=True,
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
