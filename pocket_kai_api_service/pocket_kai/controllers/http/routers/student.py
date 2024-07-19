from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, status

from pocket_kai.application.dto.student import NewStudentDTO
from pocket_kai.application.interactors.student import AddGroupMembersInteractor
from pocket_kai.controllers.http.dependencies import check_service_token
from pocket_kai.controllers.schemas.student import AddGroupMembersRequest
from pocket_kai.domain.exceptions.group import GroupNotFoundError


router = APIRouter(route_class=DishkaRoute)


@router.post(
    '/add_group_members',
    dependencies=[Depends(check_service_token)],
    include_in_schema=False,
)
async def add_group_members(
    request_data: AddGroupMembersRequest,
    *,
    interactor: FromDishka[AddGroupMembersInteractor],
):
    try:
        await interactor(
            group_name=request_data.group_name,
            members=[
                NewStudentDTO(
                    number=student.number,
                    is_leader=student.is_leader,
                    full_name=student.full_name,
                    phone=student.phone,
                    email=student.email,
                )
                for student in request_data.students
            ],
        )
    except GroupNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found',
        )
