from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.department import SADepartmentRepository
from core.repositories.discipline import SADisciplineRepository
from core.repositories.group import SAGroupRepository
from core.repositories.lesson import SALessonRepository
from core.repositories.service_token import SAServiceTokenRepository
from core.repositories.teacher import SATeacherRepository
from database.db import get_async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_lesson_repository(session: AsyncSessionDep):
    return SALessonRepository(session=session)


def get_group_repository(session: AsyncSessionDep):
    return SAGroupRepository(session=session)


def get_service_token_repository(session: AsyncSessionDep):
    return SAServiceTokenRepository(session=session)


def get_teacher_repository(session: AsyncSessionDep):
    return SATeacherRepository(session=session)


def get_department_repository(session: AsyncSessionDep):
    return SADepartmentRepository(session=session)


def get_discipline_repository(session: AsyncSessionDep):
    return SADisciplineRepository(session=session)
