from abc import abstractmethod

from typing import Protocol

from datetime import datetime

from uuid import UUID

from enum import Enum
from pydantic import BaseModel


class JWTTokenType(str, Enum):
    ACCESS_TOKEN = 'access'
    REFRESH_TOKEN = 'refresh'


class JWTPayload(BaseModel):
    sub: UUID
    type: JWTTokenType
    exp: datetime
    iat: datetime


class RefreshJWTPayload(JWTPayload):
    jti: UUID


class AccessJWTPayload(JWTPayload):
    # TODO: добавить роль и права
    pass


class JWTManagerProtocol(Protocol):
    @abstractmethod
    def decode_refresh_token(self, token: str | bytes) -> RefreshJWTPayload:
        raise NotImplementedError

    @abstractmethod
    def decode_access_token(self, token: str | bytes) -> AccessJWTPayload:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(self, user_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(
        self,
        jti: str,
        user_id: str,
        expires_at: datetime | None = None,
    ) -> str:
        raise NotImplementedError
