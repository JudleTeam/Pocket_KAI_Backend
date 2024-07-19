from datetime import datetime

import dataclasses

from pocket_kai.infrastructure.kai_parser_api.schemas import TaskStatus, TaskType


@dataclasses.dataclass(slots=True)
class TaskEntity:
    id: str
    created_at: datetime
    type: TaskType
    status: TaskStatus
    login: str | None
    group_name: str | None
    errors: str | None
    ended_at: datetime | None
