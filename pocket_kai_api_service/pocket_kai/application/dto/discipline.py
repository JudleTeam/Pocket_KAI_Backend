import dataclasses


@dataclasses.dataclass(slots=True)
class NewDisciplineDTO:
    name: str
    kai_id: int
