from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from config import Settings, get_settings
from core.security.jwt import PyJWTManager
from core.security.password import BcryptPasswordManager, PasswordManagerProtocol


@lru_cache
def get_password_manager() -> PasswordManagerProtocol:
    return BcryptPasswordManager()


@lru_cache
def get_jwt_manager(settings: Annotated[Settings, Depends(get_settings)]):
    return PyJWTManager(
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        private_key=settings.private_key_path.read_text(),
        public_key=settings.public_key_path.read_text(),
        algorithm=settings.JWT_ALGORITHM,
    )
