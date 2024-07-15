from uuid import UUID
import datetime as dt

from pydantic import BaseModel

from core.common import TaskStatus, TaskType


class TaskRead(BaseModel):
    id: UUID
    created_at: dt.datetime
    type: TaskType
    status: TaskStatus
    login: str | None
    group_name: str | None
    errors: str | None
    ended_at: dt.datetime | None
