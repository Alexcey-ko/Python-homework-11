"""Описание сущностей для Scustom."""

from pydantic import BaseModel, ConfigDict


class ScustomData(BaseModel):
    """Тип данных для объектов Scustom."""
    #Ключевые поля
    id: int|None = None
    #Вторичные поля
    email: str
    phone_number: str
    name: str | None

class ScustomAuth(BaseModel):
    """Данные авторизации."""
    id: int
    email: str
    auth: bool

    model_config = ConfigDict(frozen=True)