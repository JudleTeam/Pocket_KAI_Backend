from typing import Annotated, Union

from dishka import FromDishka
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, Query, status

from pocket_kai.application.dto.group import NewGroupDTO
from pocket_kai.application.interactors.exam import GetExamsByGroupIdInteractor
from pocket_kai.application.interactors.group import (
    CreateGroupInteractor,
    GetAllGroupsInteractor,
    GetGroupByIdInteractor,
    GetGroupByNameInteractor,
    PatchGroupByIdInteractor,
    PatchGroupByNameInteractor,
    SuggestGroupsByNameInteractor,
)
from pocket_kai.application.interactors.lesson import GetLessonsByGroupIdInteractor
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.exam import ExamRead
from pocket_kai.controllers.schemas.group import (
    FullGroupRead,
    GroupCreate,
    GroupPatch,
    ShortGroupRead,
)
from pocket_kai.controllers.schemas.lesson import LessonRead
from pocket_kai.domain.exceptions.group import (
    GroupAlreadyExistsError,
    GroupNotFoundError,
)


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '/by_id/{group_id}/lesson',
    response_model=list[LessonRead],
    responses={
        404: {
            'description': 'Группа не найдена',
            'model': ErrorMessage,
        },
    },
    name='Получить занятия группы по ID',
)
async def get_group_lessons_by_group_id(
    group_id: UUID,
    *,
    interactor: FromDishka[GetLessonsByGroupIdInteractor],
):
    """
    Возвращает список всех уроков для группы по её `ID` (ID из PocketKAI).
    """
    try:
        return await interactor(group_id=group_id)
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )


@router.get(
    '/by_id/{group_id}/exam',
    response_model=list[ExamRead],
    responses={
        404: {
            'description': 'Группа не найдена',
            'model': ErrorMessage,
        },
    },
)
async def get_group_exams_by_group_id(
    group_id: UUID,
    academic_year: str = None,
    academic_year_half: int = None,
    *,
    interactor: FromDishka[GetExamsByGroupIdInteractor],
):
    """
    Возвращает список всех экзаменов для группы по её `ID` (ID из PocketKAI).
    """
    try:
        return await interactor(
            group_id=str(group_id),
            academic_year=academic_year,
            academic_year_half=academic_year_half,
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )


@router.get(
    '/',
    response_model=Union[list[FullGroupRead], list[ShortGroupRead]],
    name='Получить все группы',
)
async def get_all_groups(
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
    offset: Annotated[int, Query(ge=0)] = 0,
    is_short: Annotated[
        bool,
        Query(description='Если `true`, то вернется сокращённая модель группы'),
    ] = True,
    *,
    interactor: FromDishka[GetAllGroupsInteractor],
):
    """
    Возвращает список всех групп с краткой либо полной (зависит от параметра `short`) информацией о них
    """
    return await interactor(limit=limit, offset=offset, is_short=is_short)


@router.get(
    '/by_name/{group_name}',
    response_model=FullGroupRead,
    responses={
        404: {
            'description': 'Группа не найдена',
            'model': ErrorMessage,
        },
    },
    name='Получить группу по номеру',
)
async def get_group_by_name(
    group_name: str,
    *,
    interactor: FromDishka[GetGroupByNameInteractor],
):
    """
    Возвращает полную информацию о группе по её имени (номеру)
    """
    try:
        return await interactor(group_name)
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Group with name "{group_name}" not found',
        )


@router.get(
    '/by_id/{group_id}',
    response_model=FullGroupRead,
    responses={
        404: {
            'description': 'Группа не найдена',
            'model': ErrorMessage,
        },
    },
    name='Получить группу по ID',
)
async def get_group_by_id(
    group_id: UUID,
    *,
    interactor: FromDishka[GetGroupByIdInteractor],
):
    """
    Возвращает полную информацию о группе по её ID (ID из PocketKAI)
    """
    try:
        return await interactor(group_id)
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Group with ID "{group_id}" not found',
        )


@router.get(
    '/suggest',
    response_model=list[ShortGroupRead],
    name='Предложить группу по имени',
)
async def suggest_group_by_name(
    group_name: str,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    *,
    interactor: FromDishka[SuggestGroupsByNameInteractor],
):
    """
    Возвращает список групп, имя (номер) которых начинается с переданного параметра `group_name`,
    с краткой информацией о них
    """
    return await interactor(group_name, limit=limit, offset=0)


@router.post(
    '/',
    dependencies=[Depends(check_service_token)],
    response_model=FullGroupRead,
    include_in_schema=False,
)
async def create_group(
    group_create: GroupCreate,
    *,
    interactor: FromDishka[CreateGroupInteractor],
):
    try:
        return await interactor(
            NewGroupDTO(group_name=group_create.group_name, kai_id=group_create.kai_id),
        )
    except GroupAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Group with provided KAI id or name already exists',
        )


@router.patch(
    '/by_name/{group_name}',
    dependencies=[Depends(check_service_token)],
    response_model=FullGroupRead,
    include_in_schema=False,
)
async def patch_group_by_name(
    group_name: str,
    group_patch: GroupPatch,
    *,
    interactor: FromDishka[PatchGroupByNameInteractor],
):
    try:
        return await interactor(
            group_name=group_name,
            group_patch=group_patch,
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )


@router.patch(
    '/by_id/{group_id}',
    dependencies=[Depends(check_service_token)],
    response_model=FullGroupRead,
    include_in_schema=False,
)
async def patch_group_by_id(
    group_id: UUID,
    group_patch: GroupPatch,
    *,
    interactor: FromDishka[PatchGroupByIdInteractor],
):
    try:
        return await interactor(
            group_id=group_id,
            group_patch=group_patch,
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )
