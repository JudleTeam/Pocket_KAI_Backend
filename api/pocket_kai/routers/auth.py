import secrets

from fastapi import APIRouter, HTTPException, status

from api.dependencies import token_service_dep, kai_user_service_dep
from api.pocket_kai.schemas.auth import LoginForm, TokenRead
from database.models.token import Token

router = APIRouter()


@router.post('/login', response_model=TokenRead)
async def login(
    login_data: LoginForm,
    token_service: token_service_dep,
    kai_user_service: kai_user_service_dep
) -> Token:
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail='Invalid credentials. Check login and password or try to register')

    kai_user = await kai_user_service.get_by_login(login_data.login)

    if kai_user is None:
        raise exception

    is_correct_password = secrets.compare_digest(
        kai_user.password.encode('utf-8'), login_data.password.encode('utf-8')
    )

    if not is_correct_password:
        raise exception

    new_token = token_service.create_token()

    return new_token
