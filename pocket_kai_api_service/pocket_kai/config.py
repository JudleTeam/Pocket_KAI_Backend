from pathlib import Path

from functools import lru_cache
from pydantic import BaseModel, computed_field

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,
        extra='allow',
    )

    # Для шифрования паролей
    SECRET_KEY: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: int = 5432

    @computed_field  # type: ignore[misc]
    @property
    def database_uri(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,
        extra='allow',
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320  # 28 days
    PRIVATE_KEY_FILE: str = 'jwt-private.pem'
    PUBLIC_KEY_FILE: str = 'jwt-public.pem'
    JWT_ALGORITHM: str = 'RS256'

    @computed_field  # type: ignore[misc]
    @property
    def private_key_path(self) -> Path:
        return BASE_DIR / 'certs' / self.PRIVATE_KEY_FILE

    @computed_field  # type: ignore[misc]
    @property
    def public_key_path(self) -> Path:
        return BASE_DIR / 'certs' / self.PUBLIC_KEY_FILE


class KaiParserSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,
        extra='allow',
    )

    KAI_PARSER_API_BASE_URL: str


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,
        extra='allow',
    )

    TEACHER_SEARCH_SIMILARITY: float = 0.15


class Settings(BaseModel):
    postgres: PostgresSettings = PostgresSettings()
    jwt: JWTSettings = JWTSettings()
    kai_parser: KaiParserSettings = KaiParserSettings()
    common: CommonSettings = CommonSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
