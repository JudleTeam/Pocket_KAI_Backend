from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        env_file='.env',
        env_file_encoding='UTF-8',
    )

    POCKET_KAI_API_URL: str
    SERVICE_TOKEN: str

    KAI_PARSER_URL: str

    UPDATE_SCHEDULE: bool = False

    TIMEZONE: str = 'Europe/Moscow'


settings = Settings()
