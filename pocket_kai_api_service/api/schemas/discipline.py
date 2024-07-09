import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DisciplineRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    created_at: datetime.datetime
    kai_id: int
    name: str


class DisciplineCreate(BaseModel):
    kai_id: int
    name: str
