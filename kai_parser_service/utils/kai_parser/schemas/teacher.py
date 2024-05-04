from pydantic import BaseModel


class Teacher(BaseModel):
    type: str
    lesson_name: str
    teacher_full_name: str
