from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True
    )

    request_retries: int = 3
    timeout_seconds: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()
