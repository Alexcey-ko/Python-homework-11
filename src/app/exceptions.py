"""Модуль содержит исключительные ситуации."""

class UserAlreadyExistsError(Exception):
    """Исключение. Пользователь уже существует."""
    def __init__(self, message: str = 'Пользователь уже существует'):
        """Инициализация сообщения."""
        super().__init__(message)

class UserDoesntExistsError(Exception):
    """Исключение. Пользователя не существует."""
    def __init__(self, message: str = 'Пользователя с таким email не существует'):
        """Инициализация сообщения."""
        super().__init__(message)

class NotEnoughSeatsError(Exception):
    """Исключение. Недостаточно мест в рейсе."""
    def __init__(self, message: str = 'Недостаточно мест в рейсе'):
        """Инициализация сообщения."""
        super().__init__(message)

class SflightNotFoundError(Exception):
    """Исключение. Рейс не найден."""
    def __init__(self, message: str = 'Рейс не найден.'):
        """Инициализация сообщения."""
        super().__init__(message)