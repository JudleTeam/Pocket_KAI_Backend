from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status

from pocket_kai.application.dto.exam import NewExamDTO, UpdateExamDTO
from pocket_kai.application.interactors.exam import (
    CreateExamInteractor,
    DeleteExamInteractor,
    UpdateExamInteractor,
)
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.exam import ExamCreate, ExamRead, ExamUpdate
from pocket_kai.domain.exceptions.exam import ExamNotFoundError


router = APIRouter(route_class=DishkaRoute)


@router.post(
    '',
    response_model=ExamRead,
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def create_new_exam(
    data: ExamCreate,
    *,
    interactor: FromDishka[CreateExamInteractor],
):
    dto = NewExamDTO(**data.model_dump())
    return await interactor(dto)


@router.put(
    '/{exam_id}',
    response_model=ExamRead,
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def update_exam(
    exam_id: UUID,
    data: ExamUpdate,
    *,
    interactor: FromDishka[UpdateExamInteractor],
):
    try:
        return await interactor(
            UpdateExamDTO(
                id=str(exam_id),
                **data.model_dump(),
            ),
        )
    except ExamNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Exam not found',
        )


@router.delete(
    '/{exam_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def delete_exam(
    exam_id: UUID,
    *,
    interactor: FromDishka[DeleteExamInteractor],
):
    await interactor(exam_id=str(exam_id))
