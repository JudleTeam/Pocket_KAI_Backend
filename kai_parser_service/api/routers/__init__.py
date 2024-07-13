from fastapi import APIRouter

from api.routers.group import router as group_router
from api.routers.schedule import router as schedule_router
from api.routers.user import router as user_router


router = APIRouter()

router.include_router(group_router, prefix='/group', tags=['Group'])
router.include_router(schedule_router, prefix='/schedule', tags=['Schedule'])
router.include_router(user_router, prefix='/user', tags=['User'])
