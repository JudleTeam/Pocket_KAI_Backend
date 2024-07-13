from typing import Annotated

from fastapi import APIRouter, Cookie, Form, HTTPException, Response

from api.dependencies import AuthServiceDep


router = APIRouter()


@router.post(
    '/login',
)
async def login_with_kai_credentials(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    auth_service: AuthServiceDep,
    response: Response,
):
    try:
        access_token, refresh_token = await auth_service.login_by_kai(
            username=login,
            password=password,
        )
    except Exception as e:
        # TODO: better error handling
        raise HTTPException(status_code=400, detail=str(e))

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
    auth_service: AuthServiceDep,
    response: Response,
):
    try:
        access_token, refresh_token = await auth_service.refresh_token_pair(
            refresh_token=refresh_token,
        )
    except Exception as e:
        # TODO: better error handling
        raise HTTPException(status_code=400, detail=str(e))

    response.set_cookie(
        key='RefreshToken',
        value=refresh_token,
        httponly=True,
        secure=True,
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
