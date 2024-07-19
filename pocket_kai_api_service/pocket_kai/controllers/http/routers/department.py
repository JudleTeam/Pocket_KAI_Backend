from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status

from pocket_kai.application.dto.department import NewDepartmentDTO
from pocket_kai.application.interactors.department import (
    CreateDepartmentInteractor,
    GetDepartmentByKaiIdInteractor,
)
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.common import ErrorMessage
from pocket_kai.controllers.schemas.department import DepartmentCreate, DepartmentRead
from pocket_kai.domain.exceptions.department import (
    DepartmentAlreadyExistsError,
    DepartmentNotFoundError,
)


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '/by_kai_id/{kai_id}',
    response_model=DepartmentRead,
    responses={
        404: {
            'description': 'Кафедра не найдена',
            'model': ErrorMessage,
        },
    },
)
async def get_department_by_kai_id(
    kai_id: int,
    *,
    interactor: FromDishka[GetDepartmentByKaiIdInteractor],
):
    """
    Возвращает кафедру по её ID в КАИ.
    *Берётся из базы данных Pocket KAI, а не сайта КАИ!*
    """
    try:
        return await interactor(kai_id)
    except DepartmentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department not found',
        )


@router.post(
    '',
    response_model=DepartmentRead,
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def create_department(
    department_create: DepartmentCreate,
    *,
    interactor: FromDishka[CreateDepartmentInteractor],
):
    try:
        return await interactor(
            NewDepartmentDTO(
                kai_id=department_create.kai_id,
                name=department_create.name,
            ),
        )
    except DepartmentAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail='Department with provided KAI id already exists',
        )
