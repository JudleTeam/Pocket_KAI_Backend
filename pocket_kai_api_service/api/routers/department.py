from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import check_service_token, DepartmentServiceDep
from api.schemas.department import DepartmentRead, DepartmentCreate
from core.exceptions.base import EntityAlreadyExistsError, EntityNotFoundError


router = APIRouter()


@router.get(
    '/by_kai_id/{kai_id}',
    response_model=DepartmentRead,
)
async def get_department_by_kai_id(
    kai_id: int,
    department_service: DepartmentServiceDep,
):
    try:
        return await department_service.get_by_kai_id(kai_id)
    except EntityNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post(
    '',
    response_model=DepartmentRead,
    dependencies=[Depends(check_service_token)],
)
async def create_department(
    department_create: DepartmentCreate,
    department_service: DepartmentServiceDep,
):
    try:
        return await department_service.create(department_create)
    except EntityAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail='Department with provided KAI id already exists',
        )
