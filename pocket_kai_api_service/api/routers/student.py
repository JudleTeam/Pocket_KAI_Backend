from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import StudentUseCaseDep, check_service_token
from api.schemas.student import AddGroupMembersRequest
from core.exceptions.base import EntityNotFoundError


router = APIRouter()


@router.post(
    '/add_group_members',
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def add_group_members(
    request_data: AddGroupMembersRequest,
    student_usecase: StudentUseCaseDep,
):
    try:
        await student_usecase.add_group_members(request_data)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
