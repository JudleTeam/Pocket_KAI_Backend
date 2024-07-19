from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from pocket_kai.infrastructure.kai_parser_api.schemas import TaskStatus, TaskType


class TaskRead(BaseModel):
    id: UUID
    created_at: datetime
    type: TaskType
    status: TaskStatus
    login: str | None
    group_name: str | None
    errors: str | None
    ended_at: datetime | None
