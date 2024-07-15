from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from fastapi import Depends, HTTPException, Header, status

from core.entities.user import UserEntity
from core.exceptions.auth import InvalidTokenError
from core.exceptions.base import EntityNotFoundError
from core.services.department import DepartmentServiceBase
from core.services.discipline import DisciplineServiceBase
from core.services.lesson import LessonServiceBase
from core.services.user import UserServiceBase
from core.services.providers import (
    get_discipline_service,
    get_lesson_service,
    get_user_service,
    get_schedule_service,
    get_service_token_service,
    get_teacher_service,
    get_department_service,
)
from core.usecases.auth import AuthUseCase
from core.services.schedule import ScheduleServiceBase
from core.services.service_token import ServiceTokenServiceBase
from core.services.teacher import TeacherServiceBase
from core.usecases.group import GroupUseCase
from core.usecases.providers import (
    get_auth_usecase,
    get_group_usecase,
    get_student_usecase,
    get_task_usecase,
)
from core.usecases.student import StudentUseCase
from core.usecases.task import TaskUseCase


LessonServiceDep = Annotated[LessonServiceBase, Depends(get_lesson_service)]
ScheduleServiceDep = Annotated[ScheduleServiceBase, Depends(get_schedule_service)]
ServiceTokenServiceDep = Annotated[
    ServiceTokenServiceBase,
    Depends(get_service_token_service),
]
TeacherServiceDep = Annotated[TeacherServiceBase, Depends(get_teacher_service)]
DepartmentServiceDep = Annotated[DepartmentServiceBase, Depends(get_department_service)]
DisciplineServiceDep = Annotated[DisciplineServiceBase, Depends(get_discipline_service)]
UserServiceDep = Annotated[UserServiceBase, Depends(get_user_service)]

GroupUseCaseDep = Annotated[GroupUseCase, Depends(get_group_usecase)]
AuthUseCaseDep = Annotated[AuthUseCase, Depends(get_auth_usecase)]
StudentUseCaseDep = Annotated[StudentUseCase, Depends(get_student_usecase)]
TaskUseCaseDep = Annotated[TaskUseCase, Depends(get_task_usecase)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def check_service_token(
    x_service_token: Annotated[str | None, Header()],
    service_token_service: ServiceTokenServiceDep,
) -> None:
    service_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Bad service token',
    )

    if x_service_token is None:
        raise service_token_exception

    try:
        await service_token_service.get_by_token(token=x_service_token)
    except EntityNotFoundError:
        raise service_token_exception


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
) -> UserEntity:
    try:
        return await user_service.get_by_access_token(access_token=token)
    except (InvalidTokenError, EntityNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


def get_current_active_user(
    current_user: Annotated[UserEntity, Depends(get_current_user)],
) -> UserEntity:
    if current_user.is_blocked:
        raise HTTPException(status_code=401, detail='Blocked user')

    return current_user
