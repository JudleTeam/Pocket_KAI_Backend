import dataclasses

from pocket_kai.domain.entitites.teacher import TeacherEntity


@dataclasses.dataclass(slots=True)
class NewDisciplineDTO:
    name: str
    kai_id: int


@dataclasses.dataclass(slots=True)
class DisciplineTypeWithTeacherDTO:
    parsed_type: str
    original_type: str
    teacher: TeacherEntity | None


@dataclasses.dataclass(slots=True)
class DisciplineWithTypesDTO:
    id: str
    kai_id: int
    name: str
    types: list[DisciplineTypeWithTeacherDTO]
