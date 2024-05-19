from uuid import UUID

from fastapi import APIRouter, HTTPException

from api.dependencies import LessonServiceDep
from api.schemas.lesson import LessonRead
from core.exceptions.base import EntityNotFoundError


router = APIRouter()


@router.get(
    '/by_id/{group_id}/lesson',
    response_model=list[LessonRead]
)
async def get_group_lessons_by_group_id(
    group_id: UUID,
    lesson_service: LessonServiceDep
):
    try:
        return await lesson_service.get_by_group_id(group_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail='Group not found')