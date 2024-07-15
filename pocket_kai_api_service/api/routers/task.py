from fastapi import APIRouter, HTTPException, status

from api.dependencies import TaskUseCaseDep
from api.schemas.task import TaskRead
from core.exceptions.kai_parser import KaiParserApiError


router = APIRouter()


@router.get(
    '',
    response_model=list[TaskRead],
)
async def get_tasks(
    limit: int = 10,
    offset: int = 0,
    group_name: str | None = None,
    login: str | None = None,
    *,
    task_usecase: TaskUseCaseDep,
):
    try:
        return await task_usecase.get_tasks(
            limit=limit,
            offset=offset,
            group_name=group_name,
            login=login,
        )
    except KaiParserApiError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='KAI parser service unavailable',
        )
