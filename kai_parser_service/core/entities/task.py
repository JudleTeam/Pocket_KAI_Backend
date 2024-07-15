from datetime import datetime

from core.common import TaskStatus, TaskType
from core.entities.base import BaseEntity


class TaskEntity(BaseEntity):
    name: str
    type: TaskType
    login: str | None
    group_name: str | None
    status: TaskStatus
    errors: str | None
    ended_at: datetime | None
