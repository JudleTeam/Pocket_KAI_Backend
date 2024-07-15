from typing import Annotated

from fastapi import Depends

from core.repositories.providers import get_task_repository
from core.repositories.task import TaskRepositoryBase
from core.services.task import TaskService
from core.unit_of_work import UnitOfWorkBase, get_uow


UOWDep = Annotated[UnitOfWorkBase, Depends(get_uow)]


def get_task_service(
    task_repository: Annotated[TaskRepositoryBase, Depends(get_task_repository)],
    uow: UOWDep,
):
    return TaskService(task_repository=task_repository, uow=uow)
