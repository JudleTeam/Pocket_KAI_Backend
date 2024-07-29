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
    exam,
)


router = APIRouter(route_class=DishkaRoute)

router.include_router(teacher.router, prefix='/teacher', tags=['Преподаватели'])
router.include_router(student.router, prefix='/student', tags=['Студенты'])
router.include_router(auth.router, prefix='/auth', tags=['Аутентификация'])
router.include_router(user.router, prefix='/user', tags=['Пользователи'])
router.include_router(common.router, prefix='', tags=['Общее'])
router.include_router(discipline.router, prefix='/discipline', tags=['Дисциплины'])
router.include_router(department.router, prefix='/department', tags=['Кафедры'])
router.include_router(lesson.router, prefix='/lesson')
router.include_router(group.router, prefix='/group', tags=['Группы'])
router.include_router(schedule.router, prefix='/group', tags=['Расписание групп'])
router.include_router(task.router, prefix='/task', tags=['Фоновые задачи'])
router.include_router(exam.router, prefix='/exam', tags=['Экзамены'])
