from typing import Annotated

from fastapi import Depends

from core.repositories.department import DepartmentRepositoryBase
from core.repositories.discipline import DisciplineRepositoryBase
from core.repositories.group import GroupRepositoryBase
from core.repositories.lesson import LessonRepositoryBase
from core.repositories.providers import (
    get_discipline_repository, get_group_repository, get_lesson_repository, get_service_token_repository,
    get_teacher_repository, get_department_repository,
)
from core.repositories.service_token import ServiceTokenRepositoryBase
from core.repositories.teacher import TeacherRepositoryBase
from core.services.department import DepartmentServiceBase, DepartmentService
from core.services.discipline import DisciplineService, DisciplineServiceBase
from core.services.group import GroupService, GroupServiceBase
from core.services.lesson import LessonService, LessonServiceBase
from core.services.schedule import ScheduleService, ScheduleServiceBase
from core.services.service_token import ServiceTokenService, ServiceTokenServiceBase
from core.services.teacher import TeacherServiceBase, TeacherService
from core.unit_of_work import UnitOfWorkBase, get_uow

UOWDep = Annotated[UnitOfWorkBase, Depends(get_uow)]


def get_group_service(
    group_repository: Annotated[GroupRepositoryBase, Depends(get_group_repository)],
    unit_of_work: UOWDep
) -> GroupServiceBase:
    return GroupService(
        group_repository=group_repository,
        uow=unit_of_work
    )


def get_lesson_service(
    lesson_repository: Annotated[LessonRepositoryBase, Depends(get_lesson_repository)],
    unit_of_work: UOWDep
) -> LessonServiceBase:
    return LessonService(
        lesson_repository=lesson_repository,
        uow=unit_of_work
    )


def get_schedule_service(
    lesson_service: Annotated[LessonServiceBase, Depends(get_lesson_service)],
    group_service: Annotated[GroupServiceBase, Depends(get_group_service)],
) -> ScheduleServiceBase:
    return ScheduleService(lesson_service=lesson_service, group_service=group_service)


def get_service_token_service(
    service_token_repository: Annotated[ServiceTokenRepositoryBase, Depends(get_service_token_repository)],
) -> ServiceTokenServiceBase:
    return ServiceTokenService(
        service_token_repository=service_token_repository
    )


def get_teacher_service(
    teacher_repository: Annotated[TeacherRepositoryBase, Depends(get_teacher_repository)],
    unit_of_work: UOWDep
) -> TeacherServiceBase:
    return TeacherService(
        teacher_repository=teacher_repository,
        uow=unit_of_work
    )


def get_department_service(
    department_repository: Annotated[DepartmentRepositoryBase, Depends(get_department_repository)],
    unit_of_work: UOWDep
) -> DepartmentServiceBase:
    return DepartmentService(
        department_repository=department_repository,
        uow=unit_of_work
    )


def get_discipline_service(
    discipline_repository: Annotated[DisciplineRepositoryBase, Depends(get_discipline_repository)],
    unit_of_work: UOWDep
) -> DisciplineServiceBase:
    return DisciplineService(
        discipline_repository=discipline_repository,
        uow=unit_of_work
    )
