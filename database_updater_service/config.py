from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        env_file='.env',
        env_file_encoding='UTF-8',
    )

    pocket_kai_api_url: str
    service_token: str

    kai_parser_url: str

    timezone: str = 'Europe/Moscow'


settings = Settings()
