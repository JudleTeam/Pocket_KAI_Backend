from pathlib import Path

from functools import lru_cache
from pydantic import computed_field

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str

    KAI_PARSER_API_BASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320  # 28 days
    PRIVATE_KEY_FILE: str = 'jwt-private.pem'
    PUBLIC_KEY_FILE: str = 'jwt-public.pem'
    JWT_ALGORITHM: str = 'RS256'

    @computed_field  # type: ignore[misc]
    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    @computed_field  # type: ignore[misc]
    @property
    def private_key_path(self) -> Path:
        return BASE_DIR / 'certs' / self.PRIVATE_KEY_FILE

    @computed_field  # type: ignore[misc]
    @property
    def public_key_path(self) -> Path:
        return BASE_DIR / 'certs' / self.PUBLIC_KEY_FILE


@lru_cache
def get_settings() -> Settings:
    return Settings()
