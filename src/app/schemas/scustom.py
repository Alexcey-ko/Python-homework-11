"""Схемы для SCUSTOM."""

import re

from pydantic import BaseModel, ConfigDict, field_validator


class ScustomLoginSchema(BaseModel):
    """Схема для авторизации пользователя."""
    email: str
    phone_number: str

class ScustomAuthSchema(BaseModel):
    """Данные авторизации пользователя."""
    id: int
    email: str
    auth: bool

    model_config = ConfigDict(frozen=True)

class ScustomSchema(BaseModel):
    """Схема пользователя."""
    id: int|None = None
    email: str
    phone_number: str
    name: str | None

    #@field_validator('phone_number')
    #@classmethod
    #def validate_phone_number(cls, values:str) -> str:
    #    """Валидация номера телефона."""
    #    if not re.match(r'^\+\d{1,15}$', values):
    #        raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
    #    return values