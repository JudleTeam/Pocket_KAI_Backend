from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.group import GroupService
from core.services.kai_user import KaiUserService
from core.services.schedule import ScheduleService
from core.services.token import TokenService
from database.base import get_async_session


def get_token_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> TokenService:
    return TokenService(session)


def get_kai_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> KaiUserService:
    return KaiUserService(session)


def get_group_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> GroupService:
    return GroupService(session)


def get_schedule_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> ScheduleService:
    return ScheduleService(session)

