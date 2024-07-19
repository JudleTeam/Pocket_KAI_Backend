from datetime import datetime

import dataclasses


@dataclasses.dataclass(slots=True)
class SpecialityEntity:
    id: str
    created_at: datetime
    kai_id: int
    code: str
    name: str
