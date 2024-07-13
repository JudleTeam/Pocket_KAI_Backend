from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Protocol
from uuid import UUID
import time

import jwt
from pydantic import BaseModel, ValidationError

from core.exceptions.auth import (
    InvalidTokenError,
    BadTokenTypeError,
    InvalidTokenPayloadError,
    InvalidTokenTypeError,
)


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
    def __init__(
        self,
        access_token_expire_minutes: int,
        refresh_token_expire_minutes: int,
        private_key: str,
        public_key: str,
        algorithm: str,
    ): ...

    def decode_jwt(
        self,
        token: str | bytes,
    ) -> dict: ...

    def decode_refresh_token(self, token: str | bytes) -> RefreshJWTPayload: ...

    def decode_access_token(self, token: str | bytes) -> AccessJWTPayload: ...

    def create_access_token(self, user_id: str) -> str: ...

    def create_refresh_token(
        self,
        jti: str,
        user_id: str,
        expires_at: datetime | None = None,
    ) -> str: ...


class PyJWTManager:
    def __init__(
        self,
        access_token_expire_minutes: int,
        refresh_token_expire_minutes: int,
        private_key: str,
        public_key: str,
        algorithm: str,
    ):
        self._ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
        self._REFRESH_TOKEN_EXPIRE_MINUTES = refresh_token_expire_minutes
        self._PRIVATE_KEY = private_key
        self._PUBLIC_KEY = public_key
        self._ALGORITHM = algorithm

    @staticmethod
    def _validate_payload(to_encode: dict) -> None:
        if to_encode.get('type') == JWTTokenType.REFRESH_TOKEN:
            payload_entity = RefreshJWTPayload
        elif to_encode.get('type') == JWTTokenType.ACCESS_TOKEN:
            payload_entity = AccessJWTPayload  # type: ignore
        else:
            raise InvalidTokenTypeError(
                message=f'Got unknown token type: {to_encode.get("type")}',
            )

        try:
            payload_entity(**to_encode)
        except ValidationError as e:
            raise InvalidTokenPayloadError(message=str(e))

    def _encode_jwt(
        self,
        payload: dict,
        expires_at: datetime,
        jti: str | None = None,
    ) -> str:
        to_encode = payload.copy()

        if jti is not None:
            to_encode.update(jti=jti)

        to_encode.update(
            exp=expires_at,
            iat=time.time(),  # Так мы исключаем вероятность создать одинаковые токены
        )

        self._validate_payload(to_encode)

        return jwt.encode(
            payload=to_encode,
            key=self._PRIVATE_KEY,
            algorithm=self._ALGORITHM,
        )

    def _decode_jwt(
        self,
        token: str | bytes,
    ) -> dict:
        try:
            return jwt.decode(
                jwt=token,
                key=self._PUBLIC_KEY,
                algorithms=[self._ALGORITHM],
            )
        except jwt.InvalidTokenError:
            raise InvalidTokenError

    def decode_refresh_token(self, token: str | bytes) -> RefreshJWTPayload:
        try:
            parsed_token_payload = RefreshJWTPayload(**self._decode_jwt(token))
        except ValidationError:
            raise InvalidTokenError(message='Bad token payload')

        if parsed_token_payload.type != JWTTokenType.REFRESH_TOKEN:
            raise BadTokenTypeError(
                message=f'Expected {JWTTokenType.REFRESH_TOKEN}, got {parsed_token_payload.type}',
            )

        return parsed_token_payload

    def decode_access_token(self, token: str | bytes) -> AccessJWTPayload:
        try:
            parsed_token_payload = AccessJWTPayload(**self._decode_jwt(token))
        except ValidationError:
            raise InvalidTokenError(message='Bad token payload')

        if parsed_token_payload.type != JWTTokenType.ACCESS_TOKEN:
            raise BadTokenTypeError(
                message=f'Expected {JWTTokenType.ACCESS_TOKEN}, got {parsed_token_payload.type}',
            )

        return parsed_token_payload

    def create_access_token(self, user_id: str) -> str:
        jwt_payload = {
            'sub': user_id,
            'type': JWTTokenType.ACCESS_TOKEN,
        }

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return self._encode_jwt(
            payload=jwt_payload,
            expires_at=expires_at,
        )

    def create_refresh_token(
        self,
        jti: str,
        user_id: str,
        expires_at: datetime | None = None,
    ) -> str:
        jwt_payload = {
            'sub': user_id,
            'type': JWTTokenType.REFRESH_TOKEN,
        }

        if expires_at is None:
            expires_at = datetime.now(timezone.utc) + timedelta(
                minutes=self._REFRESH_TOKEN_EXPIRE_MINUTES,
            )

        return self._encode_jwt(
            payload=jwt_payload,
            expires_at=expires_at,
            jti=jti,
        )
