from core.entities.base import BaseEntity
from core.entities.department import DepartmentEntity


class TeacherEntity(BaseEntity):
    login: str
    name: str

    department: DepartmentEntity
