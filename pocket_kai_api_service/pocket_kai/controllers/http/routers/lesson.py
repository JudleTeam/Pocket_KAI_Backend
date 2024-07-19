from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status

from pocket_kai.application.dto.lesson import NewLessonDTO
from pocket_kai.application.interactors.lesson import (
    CreateLessonInteractor,
    DeleteLessonInteractor,
    UpdateLessonInteractor,
)
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.lesson import LessonCreate, LessonRead, LessonUpdate
from pocket_kai.domain.entitites.lesson import LessonEntity
from pocket_kai.domain.exceptions.base import BadRelatedEntityError
from pocket_kai.domain.exceptions.lesson import LessonNotFoundError


router = APIRouter(route_class=DishkaRoute)


@router.post(
    '',
    dependencies=[Depends(check_service_token)],
    response_model=LessonRead,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_lesson(
    lesson_create: LessonCreate,
    *,
    interactor: FromDishka[CreateLessonInteractor],
):
    try:
        return await interactor(
            NewLessonDTO(
                number_of_day=lesson_create.number_of_day,
                original_dates=lesson_create.original_dates,
                parsed_parity=lesson_create.parsed_parity,
                parsed_dates=lesson_create.parsed_dates,
                parsed_dates_status=lesson_create.parsed_dates_status,
                audience_number=lesson_create.audience_number,
                building_number=lesson_create.building_number,
                original_lesson_type=lesson_create.original_lesson_type,
                parsed_lesson_type=lesson_create.parsed_lesson_type,
                start_time=lesson_create.start_time,
                end_time=lesson_create.end_time,
                discipline_id=lesson_create.discipline_id,
                teacher_id=lesson_create.teacher_id,
                department_id=lesson_create.department_id,
                group_id=lesson_create.group_id,
            ),
        )
    except BadRelatedEntityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
    *,
    interactor: FromDishka[UpdateLessonInteractor],
):
    try:
        # TODO: Заменить на дто?
        return await interactor(
            LessonEntity(
                id=lesson_id,
                created_at=lesson_update.created_at,
                number_of_day=lesson_update.number_of_day,
                original_dates=lesson_update.original_dates,
                parsed_parity=lesson_update.parsed_parity,
                parsed_dates=lesson_update.parsed_dates,
                parsed_dates_status=lesson_update.parsed_dates_status,
                start_time=lesson_update.start_time,
                end_time=lesson_update.end_time,
                audience_number=lesson_update.audience_number,
                building_number=lesson_update.building_number,
                original_lesson_type=lesson_update.original_lesson_type,
                parsed_lesson_type=lesson_update.parsed_lesson_type,
                group_id=lesson_update.group_id,
                discipline_id=lesson_update.discipline_id,
                department_id=lesson_update.department_id,
                teacher_id=lesson_update.teacher_id,
            ),
        )
    except LessonNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Lesson not found',
        )
    except BadRelatedEntityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
    *,
    interactor: FromDishka[DeleteLessonInteractor],
):
    await interactor(lesson_id=lesson_id)
