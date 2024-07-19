from dishka import FromDishka
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Cookie, Form, HTTPException, Response, status

from pocket_kai.application.interactors.kai_login import KaiLoginInteractor
from pocket_kai.application.interactors.refresh_token import RefreshTokenPairInteractor
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.domain.exceptions.auth import InvalidTokenError
from pocket_kai.domain.exceptions.kai_parser import (
    BadKaiCredentialsError,
    KaiParserApiError,
    KaiParsingError,
)
from pocket_kai.domain.exceptions.refresh_token import RefreshTokenNotFoundError


router = APIRouter(route_class=DishkaRoute)


@router.post(
    '/login',
    responses={
        401: {
            'description': 'Неверные логин или пароль',
            'model': ErrorMessage,
        },
        503: {
            'description': 'Проблемы с КАИ или сервисом парсинга КАИ. Смотри описание ошибки',
            'model': ErrorMessage,
        },
    },
    name='Войти с помощью данных КАИ',
)
async def login_with_kai_credentials(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    *,
    interactor: FromDishka[KaiLoginInteractor],
    response: Response,
):
    """
    Выполняет вход с помощью данных от личного кабинета на сайте КАИ.

    В ответ возвращает Access-токен, живущий 15 минут. Также проставляет Refresh-токен в HttpOnly cookie, живущий 28 дней.

    Может выполняться долго - от 5 до 20 секунд, зависит от скорости ответа сайта КАИ.

    Во время выполнения этого эндпоинта происходит:
    * Запрос к сайту КАИ на вход с использованием переданных данных
    * Сопоставление полученного студента по почте с тем, кто уже есть в базе данных PocketKAI
    * Если студент найден в базе, то возвращаются токены для связанного с ним пользователя.
    В противном случае создаются необходимые записи и возвращаются токены для только что созданных записей
    (Могут создаться как новый студент, так и новый пользователь)
    * Обновление данных для группы студента - проставляются специальность, направление, профиль и т.д.;
    группа отмечается как верифицированная

    Также после входа пользователя запускаются фоновые процессы с загрузкой доп. данных из личного кабинета КАИ:
    * Парсинг одногруппников, включая определение старосты (Тип: `group_members`)
    * Парсинг документов для группы (Учебный план, Образовательная программа, Календарный график) (Тип: `group_documents`)

    Фоновые задачи можно получить с помощью запроса `/task`
    """
    try:
        access_token, refresh_token = await interactor(
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
    responses={
        400: {
            'description': 'Невалидный Refresh-токен',
            'model': ErrorMessage,
        },
    },
    name='Обновить пару токенов',
)
async def refresh_token_pair(
    refresh_token: Annotated[str, Cookie(alias='RefreshToken')],
    *,
    interactor: FromDishka[RefreshTokenPairInteractor],
    response: Response,
):
    """
    Использует Refresh-токен из cookie для выпуска новой пары токенов Refresh + Access.
    В ответ возвращает Access-токен, живущий 15 минут, и проставляет новый Refresh-токен в HttpOnly cookie, живущий 28 дней.
    """
    try:
        access_token, refresh_token = await interactor(refresh_token=refresh_token)
    except (RefreshTokenNotFoundError, InvalidTokenError):
        raise HTTPException(status_code=400, detail='Invalid refresh token')

    response.set_cookie(
        key='RefreshToken',
        value=refresh_token,
        httponly=True,
        secure=True,
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
