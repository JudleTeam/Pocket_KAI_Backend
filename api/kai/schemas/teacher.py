from pydantic import BaseModel, ConfigDict

from api.kai.schemas.department import DepartmentRead


class TeacherRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    login: str
    name: str

    department: DepartmentRead
