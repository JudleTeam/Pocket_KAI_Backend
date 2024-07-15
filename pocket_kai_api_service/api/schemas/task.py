from datetime import datetime
from uuid import UUID

from api.schemas.common import TunedModel
from utils.kai_parser_api.schemas import TaskStatus, TaskType


class TaskRead(TunedModel):
    id: UUID
    created_at: datetime
    type: TaskType
    status: TaskStatus
    login: str | None
    group_name: str | None
    errors: str | None
    ended_at: datetime | None
