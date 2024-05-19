import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.schemas.department import DepartmentRead


class TeacherRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    created_at: datetime.datetime
    login: str
    name: str

    department: DepartmentRead | None


class TeacherCreate(BaseModel):
    login: str
    name: str

    department_id: UUID | None
