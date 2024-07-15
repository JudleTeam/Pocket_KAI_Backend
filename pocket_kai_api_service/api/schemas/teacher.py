import datetime
from uuid import UUID

from api.schemas.common import TunedModel


class TeacherRead(TunedModel):
    id: UUID
    created_at: datetime.datetime
    login: str
    name: str


class TeacherCreate(TunedModel):
    login: str
    name: str
