from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"
    STAGING = "staging"


class DatabaseSettings(BaseSettings):
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_ssl: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env_test", case_sensitive=False)
    debug: bool = False
    is_local_db: bool = False
    environment: Environment
    database: DatabaseSettings


local_set = Settings()
print(local_set.model_dump())
