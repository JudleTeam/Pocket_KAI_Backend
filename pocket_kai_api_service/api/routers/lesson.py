from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import LessonServiceDep, check_service_token
from api.schemas.lesson import LessonCreate, LessonRead, LessonUpdate
from core.exceptions.base import BadRelatedEntityError, EntityNotFoundError


router = APIRouter()


@router.post(
    '',
    dependencies=[Depends(check_service_token)],
    response_model=LessonRead,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_lesson(
    lesson_create: LessonCreate,
    lesson_service: LessonServiceDep,
):
    try:
        return await lesson_service.create(lesson_create)
    except BadRelatedEntityError:
        raise HTTPException(
            status_code=400,
            detail='Discipline, teacher, group or department does not exist',
        )


@router.put(
    '/{lesson_id}',
    dependencies=[Depends(check_service_token)],
    response_model=LessonRead,
    include_in_schema=False,
)
async def update_lesson(
    lesson_id: UUID,
    lesson_update: LessonUpdate,
    lesson_service: LessonServiceDep,
):
    try:
        return await lesson_service.update_by_group_id(lesson_id, lesson_update)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except BadRelatedEntityError:
        raise HTTPException(
            status_code=400,
            detail='Discipline, teacher, group or department does not exist',
        )


@router.delete(
    '/{lesson_id}',
    dependencies=[Depends(check_service_token)],
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
async def delete_lesson(
    lesson_id: UUID,
    lesson_service: LessonServiceDep,
):
    await lesson_service.delete(lesson_id)
