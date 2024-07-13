from fastapi import APIRouter

from .group import router as group_router
from .teacher import router as teacher_router
from .department import router as department_router
from .discipline import router as discipline_router
from .lesson import router as lesson_router
from .auth import router as auth_router
from .pocket_kai_user import router as user_router


router = APIRouter()

router.include_router(group_router, prefix='/group')
router.include_router(teacher_router, prefix='/teacher', tags=['Teachers'])
router.include_router(department_router, prefix='/department', tags=['Departments'])
router.include_router(discipline_router, prefix='/discipline', tags=['Disciplines'])
router.include_router(lesson_router, prefix='/lesson', tags=['Lessons'])
router.include_router(auth_router, prefix='/auth', tags=['Auth'])
router.include_router(user_router, prefix='/user', tags=['User'])
