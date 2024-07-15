from fastapi import Depends
from typing import Annotated

from core.security.jwt import JWTManagerProtocol
from core.security.providers import get_jwt_manager
from core.services.group import GroupServiceBase
from core.services.providers import (
    get_group_service,
    get_refresh_token_service,
    get_student_service,
    get_user_service,
)
from core.services.refresh_token import RefreshTokenServiceBase
from core.services.student import StudentServiceBase
from core.services.user import UserServiceBase
from core.usecases.auth import AuthUseCase
from core.unit_of_work import UnitOfWorkBase, get_uow
from core.usecases.group import GroupUseCase
from core.usecases.student import StudentUseCase
from core.usecases.task import TaskUseCase
from utils.kai_parser_api.api import KaiParserApi
from utils.kai_parser_api.providers import get_kai_parser_api


UowDep = Annotated[UnitOfWorkBase, Depends(get_uow)]


def get_auth_usecase(
    student_service: Annotated[StudentServiceBase, Depends(get_student_service)],
    group_service: Annotated[GroupServiceBase, Depends(get_group_service)],
    user_service: Annotated[UserServiceBase, Depends(get_user_service)],
    refresh_token_service: Annotated[
        RefreshTokenServiceBase,
        Depends(get_refresh_token_service),
    ],
    kai_parser_api: Annotated[KaiParserApi, Depends(get_kai_parser_api)],
    jwt_manager: Annotated[JWTManagerProtocol, Depends(get_jwt_manager)],
    uow: UowDep,
) -> AuthUseCase:
    return AuthUseCase(
        student_service=student_service,
        group_service=group_service,
        user_service=user_service,
        refresh_token_service=refresh_token_service,
        kai_parser_api=kai_parser_api,
        jwt_manager=jwt_manager,
        uow=uow,
    )


def get_student_usecase(
    student_service: Annotated[StudentServiceBase, Depends(get_student_service)],
    group_service: Annotated[GroupServiceBase, Depends(get_group_service)],
    uow: UowDep,
) -> StudentUseCase:
    return StudentUseCase(
        student_service=student_service,
        group_service=group_service,
        uow=uow,
    )


def get_task_usecase(
    kai_parser_api: Annotated[KaiParserApi, Depends(get_kai_parser_api)],
) -> TaskUseCase:
    return TaskUseCase(
        kai_parser_api=kai_parser_api,
    )


def get_group_usecase(
    group_service: Annotated[GroupServiceBase, Depends(get_group_service)],
    uow: UowDep,
) -> GroupUseCase:
    return GroupUseCase(
        group_service=group_service,
        uow=uow,
    )
