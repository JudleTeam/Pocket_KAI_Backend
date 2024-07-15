from typing import Annotated

from fastapi import APIRouter, Query

from api.dependencies import TaskServiceDep
from api.schemas.task import TaskRead


router = APIRouter()


@router.get(
    '/',
    response_model=list[TaskRead],
)
async def get_all_tasks(
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    group_name: str | None = None,
    login: str | None = None,
    *,
    task_service: TaskServiceDep,
):
    return await task_service.get(
        limit=limit,
        offset=offset,
        group_name=group_name,
        login=login,
    )
