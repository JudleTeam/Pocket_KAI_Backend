import datetime
from uuid import UUID

from api.schemas.common import TunedModel


class DisciplineRead(TunedModel):
    id: UUID
    created_at: datetime.datetime
    kai_id: int
    name: str


class DisciplineCreate(TunedModel):
    kai_id: int
    name: str
