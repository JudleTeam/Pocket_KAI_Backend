from pydantic import BaseModel


class GroupRead(BaseModel):
    forma: str
    name: str
    id: int
