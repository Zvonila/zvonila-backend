import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRESQL_USERNAME: str = ""
    POSTGRESQL_PASSWORD: str = ""
    POSTGRESQL_DB_NAME: str = ""
    POSTGRESQL_PORT: int = 5432
    POSTGRESQL_HOST: str = "localhost"
    PRIVATE_KEY_PATH: str = ""
    PUBLIC_KEY_PATH: str = ""
    HMAC_SECRET_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
        
settings = Settings()