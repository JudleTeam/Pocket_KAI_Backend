from fastapi import APIRouter

from .login import router as login_router
from .group import router as group_router
from .schedule import router as schedule_router


router = APIRouter()

# router.include_router(login_router)
router.include_router(group_router, prefix='/groups', tags=['Groups'])
router.include_router(schedule_router, prefix='', tags=['Schedule'])
