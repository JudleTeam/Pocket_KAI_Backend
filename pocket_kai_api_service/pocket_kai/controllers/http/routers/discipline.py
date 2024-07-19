from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status

from pocket_kai.application.dto.discipline import NewDisciplineDTO
from pocket_kai.application.interactors.discipline import (
    CreateDisciplineInteractor,
    GetDisciplineByKaiIdInteractor,
)
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.discipline import DisciplineCreate, DisciplineRead
from pocket_kai.domain.exceptions.discipline import (
    DisciplineAlreadyExistsError,
    DisciplineNotFoundError,
)


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '/by_kai_id/{kai_id}',
    response_model=DisciplineRead,
    responses={
        404: {
            'description': 'Дисциплина не найдена',
            'model': ErrorMessage,
        },
    },
)
async def get_discipline_by_kai_id(
    kai_id: int,
    *,
    interactor: FromDishka[GetDisciplineByKaiIdInteractor],
):
    """
    Возвращает дисциплину по её ID в КАИ.
    *Берётся из базы данных Pocket KAI, а не сайта КАИ!*
    """
    try:
        return await interactor(kai_id=kai_id)
    except DisciplineNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Discipline not found',
        )


@router.post(
    '',
    response_model=DisciplineRead,
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def create_discipline(
    new_discipline: DisciplineCreate,
    *,
    interactor: FromDishka[CreateDisciplineInteractor],
):
    try:
        return await interactor(
            NewDisciplineDTO(
                kai_id=new_discipline.kai_id,
                name=new_discipline.name,
            ),
        )
    except DisciplineAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail='Discipline with provided KAI id already exists',
        )
