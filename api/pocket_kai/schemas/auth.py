from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LoginForm(BaseModel):
    login: str
    password: str


class TokenRead(BaseModel):
    id: int
    token: UUID
    created_at: datetime
