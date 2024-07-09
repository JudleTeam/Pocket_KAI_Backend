from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import DisciplineServiceDep, check_service_token
from api.schemas.discipline import DisciplineCreate, DisciplineRead
from core.exceptions.base import EntityAlreadyExistsError, EntityNotFoundError


router = APIRouter()


@router.get(
    '/by_kai_id/{kai_id}',
    response_model=DisciplineRead,
)
async def get_discipline_by_kai_id(
    kai_id: int,
    discipline_service: DisciplineServiceDep,
):
    try:
        return await discipline_service.get_by_kai_id(kai_id)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post(
    '',
    response_model=DisciplineRead,
    dependencies=[Depends(check_service_token)],
)
async def create_discipline(
    new_discipline: DisciplineCreate,
    discipline_service: DisciplineServiceDep,
):
    try:
        return await discipline_service.create(new_discipline)
    except EntityAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail='Discipline with provided KAI id already exists',
        )
