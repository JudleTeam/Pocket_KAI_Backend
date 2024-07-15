from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID = None
    created_at: datetime = None
