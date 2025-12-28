"""Модуль с настройками авторизации."""

from authx import AuthX, AuthXConfig

from app.config import config

auth_config = AuthXConfig(
    JWT_SECRET_KEY = config.JWT_SECRET_KEY,
    JWT_ACCESS_COOKIE_NAME = config.JWT_ACCESS_COOKIE_NAME,
    JWT_TOKEN_LOCATION = config.JWT_TOKEN_LOCATION,
    JWT_COOKIE_CSRF_PROTECT = False,
)

security = AuthX(config = auth_config)
