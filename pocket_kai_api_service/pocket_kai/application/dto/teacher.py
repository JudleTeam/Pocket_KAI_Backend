import dataclasses


@dataclasses.dataclass(slots=True)
class NewTeacherDTO:
    name: str
    login: str
