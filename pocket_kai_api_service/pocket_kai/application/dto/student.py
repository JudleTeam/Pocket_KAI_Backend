import dataclasses


@dataclasses.dataclass(slots=True)
class NewStudentDTO:
    number: int
    is_leader: bool
    full_name: str
    phone: str | None
    email: str
