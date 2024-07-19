from datetime import datetime
import dataclasses


@dataclasses.dataclass(slots=True)
class ProfileEntity:
    id: str
    created_at: datetime
    kai_id: int
    name: str
