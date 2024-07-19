from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from pocket_kai.controllers.http.routers import (
    auth,
    student,
    teacher,
    user,
    common,
    discipline,
    department,
    lesson,
    group,
    schedule,
    task,
)


router = APIRouter(route_class=DishkaRoute)

router.include_router(teacher.router, prefix='/teacher', tags=['Teachers'])
router.include_router(student.router, prefix='/student', tags=['Students'])
router.include_router(auth.router, prefix='/auth', tags=['Auth'])
router.include_router(user.router, prefix='/user', tags=['Users'])
router.include_router(common.router, prefix='', tags=['Common'])
router.include_router(discipline.router, prefix='/discipline', tags=['Disciplines'])
router.include_router(department.router, prefix='/department', tags=['Departments'])
router.include_router(lesson.router, prefix='/lesson', tags=['Lessons'])
router.include_router(group.router, prefix='/group', tags=['Groups'])
router.include_router(schedule.router, prefix='/group', tags=['Groups Schedule'])
router.include_router(task.router, prefix='/task', tags=['Tasks'])
