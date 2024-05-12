from fastapi import APIRouter

from .group import router as group_router
from .schedule import router as group_schedule_router
from .lesson import router as group_lesson_router


router = APIRouter()

router.include_router(group_router, tags=["Groups"])
router.include_router(group_schedule_router, tags=["Groups schedule"])
router.include_router(group_lesson_router, tags=["Groups lessons"])
