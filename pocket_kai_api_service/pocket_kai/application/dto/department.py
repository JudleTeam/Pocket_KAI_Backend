import dataclasses


@dataclasses.dataclass(slots=True)
class NewDepartmentDTO:
    kai_id: int
    name: str
