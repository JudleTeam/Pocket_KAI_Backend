import datetime
from uuid import UUID

from api.schemas.common import TunedModel
from api.schemas.department import DepartmentRead


class TeacherRead(TunedModel):
    id: UUID
    created_at: datetime.datetime
    login: str
    name: str

    department: DepartmentRead | None


class TeacherCreate(TunedModel):
    login: str
    name: str

    department_id: UUID | None
