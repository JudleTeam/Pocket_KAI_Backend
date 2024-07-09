from typing import Annotated

from fastapi import Depends, HTTPException, Header, status

from core.exceptions.base import EntityNotFoundError
from core.services.department import DepartmentServiceBase
from core.services.discipline import DisciplineServiceBase
from core.services.group import GroupServiceBase
from core.services.lesson import LessonServiceBase
from core.services.providers import (
    get_discipline_service,
    get_lesson_service,
    get_schedule_service,
    get_group_service,
    get_service_token_service,
    get_teacher_service,
    get_department_service,
)
from core.services.schedule import ScheduleServiceBase
from core.services.service_token import ServiceTokenServiceBase
from core.services.teacher import TeacherServiceBase


GroupServiceDep = Annotated[GroupServiceBase, Depends(get_group_service)]
LessonServiceDep = Annotated[LessonServiceBase, Depends(get_lesson_service)]
ScheduleServiceDep = Annotated[ScheduleServiceBase, Depends(get_schedule_service)]
ServiceTokenServiceDep = Annotated[
    ServiceTokenServiceBase,
    Depends(get_service_token_service),
]
TeacherServiceDep = Annotated[TeacherServiceBase, Depends(get_teacher_service)]
DepartmentServiceDep = Annotated[DepartmentServiceBase, Depends(get_department_service)]
DisciplineServiceDep = Annotated[DisciplineServiceBase, Depends(get_discipline_service)]


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
