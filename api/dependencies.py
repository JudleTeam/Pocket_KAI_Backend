from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.group import GroupService
from core.services.kai_user import KaiUserService
from core.services.providers import get_schedule_service, get_token_service, get_kai_user_service, get_group_service
from core.services.schedule import ScheduleService
from core.services.token import TokenService
from database.base import get_async_session


TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]
KaiUserServiceDep = Annotated[KaiUserService, Depends(get_kai_user_service)]
GroupServiceDep = Annotated[GroupService, Depends(get_group_service)]
ScheduleServiceDep = Annotated[ScheduleService, Depends(get_schedule_service)]
