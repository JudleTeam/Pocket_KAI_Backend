from datetime import datetime

import dataclasses


@dataclasses.dataclass(slots=True)
class DepartmentEntity:
    id: str
    created_at: datetime
    kai_id: int
    name: str
