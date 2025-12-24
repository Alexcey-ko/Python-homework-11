"""Конфигурация приложения."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Класс с настройками приложения и параметрами из .env."""
    #DB
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    POSTGRES_HOST:str = 'localhost'
    POSTGRES_PORT:int = 5432

    #CACHE
    REDIS_URL:str = 'localhost'
    REDIS_PORT:int = 6379
    REDIS_USER:str
    REDIS_USER_PASSWORD:str
    REDIS_PASSWORD:str

    #pydantic
    model_config = SettingsConfigDict(frozen = True, extra = 'allow', env_file = '.env', env_file_encoding = 'utf-8')

config = Config()