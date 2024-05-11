from typing import Annotated, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.dependencies import GroupServiceDep, check_service_token
from api.schemas.common import ErrorMessage
from api.schemas.group import GroupCreate, GroupUpdate, ShortGroupRead, FullGroupRead
from core.exceptions.base import BadRelatedEntityError, EntityAlreadyExistsError, EntityNotFoundError


router = APIRouter()


@router.get(
    '/',
    response_model=Union[list[FullGroupRead], list[ShortGroupRead]],
)
async def get_all_groups(
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
    offset: Annotated[int, Query(ge=0)] = 0,
    is_short: Annotated[bool, Query(description='Если `true`, то вернется сокращённая модель группы')] = True,
    *,
    group_service: GroupServiceDep
):
    """
    Возвращает список всех групп с краткой либо полной (зависит от параметра `short`) информацией о них
    """
    groups = await group_service.get_all(limit=limit, offset=offset)
    if is_short:
        return [ShortGroupRead.model_validate(group) for group in groups]
    else:
        return groups


@router.get(
    '/by_name/{group_name}',
    response_model=FullGroupRead,
    responses={
        404: {
            'description': 'Group not found',
            'model'      : ErrorMessage
        }
    }
)
async def get_group_by_name(
    group_name: str,
    group_service: GroupServiceDep
):
    """
    Возвращает полную информацию о группе по её имени (номеру)
    """
    try:
        return await group_service.get_by_name(group_name)
    except EntityNotFoundError:
        raise HTTPException(
            status_code=404, detail=f'Group with name "{group_name}" not found'
        )


@router.get(
    '/by_id/{group_id}',
    response_model=FullGroupRead,
    responses={
        404: {
            'description': 'Group not found',
            'model'      : ErrorMessage
        }
    }
)
async def get_group_by_id(
    group_id: UUID,
    group_service: GroupServiceDep
):
    """
    Возвращает полную информацию о группе по её ID (ID из PocketKAI)
    """
    try:
        return await group_service.get_by_id(group_id)
    except EntityNotFoundError:
        raise HTTPException(
            status_code=404, detail=f'Group with ID "{group_id}" not found'
        )


@router.get('/suggest', response_model=list[ShortGroupRead])
async def suggest_group_by_name(
    group_name: str,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    *,
    group_service: GroupServiceDep
):
    """
    Возвращает список групп, имя (номер) которых начинается с переданного параметра `group_name`,
    с краткой информацией о них
    """
    return await group_service.suggest_by_name(group_name, limit=limit)


@router.post(
    '/',
    dependencies=[Depends(check_service_token)],
    response_model=FullGroupRead,
)
async def create_group(
    group_create: GroupCreate,
    group_service: GroupServiceDep
):
    try:
        return await group_service.create(group_create)
    except EntityAlreadyExistsError:
        raise HTTPException(
            status_code=429,
            detail='Group with provided KAI id already exists'
        )


@router.put(
    '/by_id/{group_id}',
    dependencies=[Depends(check_service_token)],
    response_model=FullGroupRead,
)
async def update_group(
    group_id: UUID,
    group_update: GroupUpdate,
    group_service: GroupServiceDep
):
    try:
        return await group_service.update(group_id, group_update)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except BadRelatedEntityError:
        raise HTTPException(status_code=400, detail='Group leader not found')
