from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.department import SADepartmentRepository
from core.repositories.discipline import SADisciplineRepository
from core.repositories.group import SAGroupRepository
from core.repositories.institute import SAInstituteRepository
from core.repositories.profile import SAProfileRepository
from core.repositories.speciality import SASpecialityRepository
from core.repositories.student import SAStudentRepository
from core.repositories.lesson import SALessonRepository
from core.repositories.user import SAUserRepository
from core.repositories.refresh_token import SARefreshTokenRepository
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


def get_user_repository(session: AsyncSessionDep):
    return SAUserRepository(session=session)


def get_student_repository(session: AsyncSessionDep):
    return SAStudentRepository(session=session)


def get_refresh_token_repository(session: AsyncSessionDep):
    return SARefreshTokenRepository(session=session)


def get_profile_repository(session: AsyncSessionDep):
    return SAProfileRepository(session=session)


def get_speciality_repository(session: AsyncSessionDep):
    return SASpecialityRepository(session=session)


def get_institute_repository(session: AsyncSessionDep):
    return SAInstituteRepository(session=session)
