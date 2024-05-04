from typing import Annotated

from fastapi import Depends

from core.repositories.group import GroupRepositoryBase
from core.repositories.lesson import LessonRepositoryBase
from core.repositories.providers import get_group_repository, get_lesson_repository
from core.services.group import GroupService, GroupServiceBase
from core.services.lesson import LessonService, LessonServiceBase
from core.services.schedule import ScheduleService, ScheduleServiceBase


def get_group_service(
    group_repository: Annotated[GroupRepositoryBase, Depends(get_group_repository)]
) -> GroupServiceBase:
    return GroupService(
        group_repository=group_repository
    )


def get_lesson_service(
    lesson_repository: Annotated[LessonRepositoryBase, Depends(get_lesson_repository)]
) -> LessonServiceBase:
    return LessonService(
        lesson_repository=lesson_repository
    )


def get_schedule_service(
    lesson_service: Annotated[LessonServiceBase, Depends(get_lesson_service)],
    group_service: Annotated[GroupServiceBase, Depends(get_group_service)],
) -> ScheduleServiceBase:
    return ScheduleService(lesson_service=lesson_service, group_service=group_service)
