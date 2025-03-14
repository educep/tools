from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"
    STAGING = "staging"


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env_test", case_sensitive=False)
    database_name: str = "default_db"
    database_user: str = "default_user"
    database_password: str = "default_password"
    database_host: str = "localhost"
    database_port: int = 5432
    database_ssl: int = 0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env_test", case_sensitive=False)
    debug: bool = False
    is_local_db: bool = False
    environment: Environment = Environment.DEV
    database: DatabaseSettings = DatabaseSettings()


local_set = Settings()
print(local_set.model_dump())
