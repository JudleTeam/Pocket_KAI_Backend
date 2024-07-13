from typing import Protocol

import bcrypt


class PasswordManagerProtocol(Protocol):
    def hash_password(self, password: str) -> bytes:
        raise NotImplementedError

    def verify_password(self, password: str, hashed_password: bytes) -> bool:
        raise NotImplementedError


class BcryptPasswordManager(PasswordManagerProtocol):
    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(
            password=password.encode('utf-8'),
            salt=bcrypt.gensalt(),
        )

    def verify_password(self, password: str | bytes, hashed_password: bytes) -> bool:
        if isinstance(password, str):
            password = password.encode('utf-8')

        return bcrypt.checkpw(
            hashed_password=hashed_password,
            password=password,
        )
