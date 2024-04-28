from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.kai_user import KaiUserService
from core.services.token import TokenService
from database.base import get_async_session


db_session_dep = Annotated[AsyncSession, Depends(get_async_session)]


def get_token_service(session: db_session_dep) -> TokenService:
    return TokenService(session)


def get_kai_user_service(session: db_session_dep) -> KaiUserService:
    return KaiUserService(session)


token_service_dep = Annotated[TokenService, Depends(get_token_service)]
kai_user_service_dep = Annotated[KaiUserService, Depends(get_kai_user_service)]
