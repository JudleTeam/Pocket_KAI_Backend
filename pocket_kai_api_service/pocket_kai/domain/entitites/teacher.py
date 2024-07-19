from datetime import datetime

import dataclasses


@dataclasses.dataclass(slots=True)
class TeacherEntity:
    id: str
    created_at: datetime
    login: str
    name: str
