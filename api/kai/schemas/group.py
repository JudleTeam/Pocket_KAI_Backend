from pydantic import BaseModel


class GroupBase(BaseModel):
    pass


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    group_id: int
