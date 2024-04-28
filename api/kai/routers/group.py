from fastapi import APIRouter

from api.kai.schemas.group import GroupCreate

router = APIRouter()


@router.post('/')
async def add_group(group: GroupCreate):
    pass


@router.post('/bulk')
async def add_groups(groups: list[GroupCreate]):
    pass
