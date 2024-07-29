from fastapi import APIRouter

from api.routers.group import router as group_router
from api.routers.schedule import router as schedule_router
from api.routers.user import router as user_router
from api.routers.task import router as task_router
from api.routers.exam import router as exam_router


router = APIRouter()

router.include_router(group_router, prefix='/group', tags=['Group'])
router.include_router(schedule_router, prefix='/schedule', tags=['Schedule'])
router.include_router(exam_router, prefix='/exam', tags=['Exam'])
router.include_router(user_router, prefix='/user', tags=['User'])
router.include_router(task_router, prefix='/task', tags=['Task'])
