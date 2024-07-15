from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.task import SATaskRepository
from database.db import get_async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_task_repository(session: AsyncSessionDep):
    return SATaskRepository(session=session)
