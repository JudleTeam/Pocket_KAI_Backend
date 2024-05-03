from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.group import SAGroupRepository
from core.repositories.lesson import SALessonRepository
from database.base import get_async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_lesson_repository(session: AsyncSessionDep):
    return SALessonRepository(session=session)


def get_group_repository(session: AsyncSessionDep):
    return SAGroupRepository(session=session)
