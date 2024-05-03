from pydantic import BaseModel, ConfigDict


class DepartmentRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    kai_id: int
    name: str
