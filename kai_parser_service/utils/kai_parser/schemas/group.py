from pydantic import BaseModel


class ParsedGroup(BaseModel):
    forma: str
    name: str
    id: int


class Documents(BaseModel):
    syllabus: str | None
    educational_program: str | None
    study_schedule: str | None
