from datetime import datetime

import dataclasses


@dataclasses.dataclass
class DisciplineEntity:
    id: str
    created_at: datetime
    kai_id: int
    name: str
