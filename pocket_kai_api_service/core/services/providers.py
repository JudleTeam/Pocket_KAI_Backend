from typing import Annotated

from fastapi import Depends

from core.repositories.department import DepartmentRepositoryBase
from core.repositories.discipline import DisciplineRepositoryBase
from core.repositories.group import GroupRepositoryBase
from core.repositories.kai_user import KaiUserRepositoryBase
from core.repositories.lesson import LessonRepositoryBase
from core.repositories.pocket_kai_user import PocketKaiUserRepositoryBase
from core.repositories.providers import (
    get_discipline_repository,
    get_group_repository,
    get_kai_user_repository,
    get_lesson_repository,
    get_pocket_kai_user_repository,
    get_refresh_token_repository,
    get_service_token_repository,
    get_teacher_repository,
    get_department_repository,
)
from core.repositories.refresh_token import RefreshTokenRepositoryBase
from core.repositories.service_token import ServiceTokenRepositoryBase
from core.repositories.teacher import TeacherRepositoryBase
from core.security.jwt import JWTManagerProtocol
from core.security.providers import get_jwt_manager
from core.services.auth import AuthService, AuthServiceBase
from core.services.department import DepartmentServiceBase, DepartmentService
from core.services.discipline import DisciplineService, DisciplineServiceBase
from core.services.group import GroupService, GroupServiceBase
from core.services.kai_user import KaiUserService, KaiUserServiceBase
from core.services.lesson import LessonService, LessonServiceBase
from core.services.pocket_kai_user import PocketKaiUserService, PocketKaiUserServiceBase
from core.services.schedule import ScheduleService, ScheduleServiceBase
from core.services.service_token import ServiceTokenService, ServiceTokenServiceBase
from core.services.teacher import TeacherServiceBase, TeacherService
from core.unit_of_work import UnitOfWorkBase, get_uow
from utils.kai_parser_api.api import KaiParserApi
from utils.kai_parser_api.providers import get_kai_parser_api


UOWDep = Annotated[UnitOfWorkBase, Depends(get_uow)]


def get_group_service(
    group_repository: Annotated[GroupRepositoryBase, Depends(get_group_repository)],
    unit_of_work: UOWDep,
) -> GroupServiceBase:
    return GroupService(
        group_repository=group_repository,
        uow=unit_of_work,
    )


def get_lesson_service(
    lesson_repository: Annotated[LessonRepositoryBase, Depends(get_lesson_repository)],
    unit_of_work: UOWDep,
) -> LessonServiceBase:
    return LessonService(
        lesson_repository=lesson_repository,
        uow=unit_of_work,
    )


def get_schedule_service(
    lesson_repository: Annotated[LessonRepositoryBase, Depends(get_lesson_repository)],
    group_repository: Annotated[GroupRepositoryBase, Depends(get_group_repository)],
) -> ScheduleServiceBase:
    return ScheduleService(
        lesson_repository=lesson_repository,
        group_repository=group_repository,
    )


def get_service_token_service(
    service_token_repository: Annotated[
        ServiceTokenRepositoryBase,
        Depends(get_service_token_repository),
    ],
) -> ServiceTokenServiceBase:
    return ServiceTokenService(
        service_token_repository=service_token_repository,
    )


def get_teacher_service(
    teacher_repository: Annotated[
        TeacherRepositoryBase,
        Depends(get_teacher_repository),
    ],
    unit_of_work: UOWDep,
) -> TeacherServiceBase:
    return TeacherService(
        teacher_repository=teacher_repository,
        uow=unit_of_work,
    )


def get_department_service(
    department_repository: Annotated[
        DepartmentRepositoryBase,
        Depends(get_department_repository),
    ],
    unit_of_work: UOWDep,
) -> DepartmentServiceBase:
    return DepartmentService(
        department_repository=department_repository,
        uow=unit_of_work,
    )


def get_discipline_service(
    discipline_repository: Annotated[
        DisciplineRepositoryBase,
        Depends(get_discipline_repository),
    ],
    unit_of_work: UOWDep,
) -> DisciplineServiceBase:
    return DisciplineService(
        discipline_repository=discipline_repository,
        uow=unit_of_work,
    )


def get_pocket_kai_user_service(
    pocket_kai_user_repository: Annotated[
        PocketKaiUserRepositoryBase,
        Depends(get_pocket_kai_user_repository),
    ],
    unit_of_work: UOWDep,
    jwt_manager: Annotated[JWTManagerProtocol, Depends(get_jwt_manager)],
) -> PocketKaiUserServiceBase:
    return PocketKaiUserService(
        pocket_kai_user_repository=pocket_kai_user_repository,
        uow=unit_of_work,
        jwt_manager=jwt_manager,
    )


def get_kai_user_service(
    kai_user_repository: Annotated[
        KaiUserRepositoryBase,
        Depends(get_kai_user_repository),
    ],
    unit_of_work: UOWDep,
) -> KaiUserServiceBase:
    return KaiUserService(
        kai_user_repository=kai_user_repository,
        uow=unit_of_work,
    )


def get_auth_service(
    pocket_kai_user_repository: Annotated[
        PocketKaiUserRepositoryBase,
        Depends(get_pocket_kai_user_repository),
    ],
    kai_user_repository: Annotated[
        KaiUserRepositoryBase,
        Depends(get_kai_user_repository),
    ],
    refresh_token_repository: Annotated[
        RefreshTokenRepositoryBase,
        Depends(get_refresh_token_repository),
    ],
    group_repository: Annotated[GroupRepositoryBase, Depends(get_group_repository)],
    uow: UOWDep,
    kai_parser_api: Annotated[KaiParserApi, Depends(get_kai_parser_api)],
    jwt_manager: Annotated[JWTManagerProtocol, Depends(get_jwt_manager)],
) -> AuthServiceBase:
    return AuthService(
        pocket_kai_user_repository=pocket_kai_user_repository,
        kai_user_repository=kai_user_repository,
        refresh_token_repository=refresh_token_repository,
        group_repository=group_repository,
        uow=uow,
        kai_parser_api=kai_parser_api,
        jwt_manager=jwt_manager,
    )
