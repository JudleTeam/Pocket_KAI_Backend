from datetime import datetime

import dataclasses


@dataclasses.dataclass(slots=True)
class ServiceTokenEntity:
    id: str
    token: str
    created_at: datetime
