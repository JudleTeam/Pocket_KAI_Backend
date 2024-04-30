from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from api.dependencies import GroupServiceDep
from api.kai.schemas.group import ShortGroupRead, FullGroupRead
from core.services.group import GroupNotFoundError


router = APIRouter()


@router.get(
    '',
    response_model=list[ShortGroupRead]
)
async def get_all_groups(
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
    offset: Annotated[int, Query(ge=0)] = 0,
    *,
    group_service: GroupServiceDep
):
    return await group_service.get_all(limit=limit, offset=offset)


@router.get(
    '/by_name/{group_name}',
    response_model=FullGroupRead
)
async def get_group_by_name(
    group_name: str,
    group_service: GroupServiceDep
):
    try:
        return await group_service.get_by_name(group_name)
    except GroupNotFoundError:
        raise HTTPException(
            status_code=404, detail=f'Group with name "{group_name}" not found'
        )


@router.get(
    '/by_id/{group_id}',
    response_model=FullGroupRead
)
async def get_group_by_id(
    group_id: UUID,
    group_service: GroupServiceDep
):
    try:
        return await group_service.get_by_id(group_id)
    except GroupNotFoundError:
        raise HTTPException(
            status_code=404, detail=f'Group with ID "{group_id}" not found'
        )


@router.get('/suggest/{group_name}', response_model=list[ShortGroupRead])
async def suggest_group_by_name(
    group_name: str,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    *,
    group_service: GroupServiceDep
):
    return await group_service.suggest_by_name(group_name, limit=limit)
