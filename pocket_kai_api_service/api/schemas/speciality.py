from datetime import datetime
from uuid import UUID

from api.schemas.common import TunedModel


class SpecialityRead(TunedModel):
    id: UUID
    created_at: datetime
    kai_id: int
    code: str
    name: str
