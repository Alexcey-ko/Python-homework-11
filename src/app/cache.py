"""Модуль для работы с REDIS кэшем."""

import contextlib
import functools
from typing import Dict

import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

from app.config import config

CACHE_DB: int = 0
REMOTE_DB: int = 1

def lazy_connect(db: int):
    """Декоратор, который лениво (по требованию) создаёт подключение к Redis для нужной базы.

    Если соединение для указанного db ещё не установлено, оно создаётся автоматически.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Проверяем, есть ли уже соединение для этой базы
            if db not in self.connections:
                # Если нет — создаём
                self.connections[db] = self.setup_connection(db=db)
            # Вызываем исходную функцию
            res = func(self, *args, **kwargs)
            return res
        return wrapper
    return decorator


class Cache:
    """Класс-обёртка для работы с Redis.

    Позволяет автоматически подключаться, хранить кэш и работать с удалёнными данными.
    """

    def __init__(self, host, port, username, password):
        """Инициализация настроек REDIS."""
        # Здесь будут храниться активные соединения к разным Redis DB (по номеру базы)
        self.connections: Dict[int, redis.Redis] = {}
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    def setup_connection(self, db: int) -> redis.Redis:
        """Создаёт подключение к Redis для указанного номера базы данных.

        Настраивает автоматические повторы при ошибках соединения.
        """
        connection = redis.Redis(
            host = self._host or config.REDIS_URL,
            port = self._port or config.REDIS_PORT,
            db = db,
            username = self._username or config.REDIS_USER,
            password = self._password or config.REDIS_USER_PASSWORD,
            #Повторные попытки с увеличением задержки
            retry = Retry(ExponentialBackoff(cap=10, base=1), retries=25),  
            #Повторять при этих типах ошибок
            retry_on_error = [ConnectionError, TimeoutError, ConnectionResetError], 
            #Проверка "живости" соединения каждые 1 секунду
            health_check_interval = 1, 
        )
        return connection

    @lazy_connect(REMOTE_DB)
    def get(self, key, db=REMOTE_DB) -> str | None:
        """Получает значение по ключу из Redis (удалённая база данных).
        
        Возвращает строку или None, если ключ не найден.
        """
        binary = self.connections[db].get(key)  # Получаем значение в виде байтов
        return binary.decode('utf-8') if binary is not None else None  # Декодируем в строку

    @lazy_connect(REMOTE_DB)
    def set(self, key, value, period, db=REMOTE_DB) -> None:
        """Сохраняет значение по ключу в Redis с возможностью указать срок жизни (TTL)."""
        self.connections[db].set(key, value)
        if isinstance(period, int) and period > 0:
            # Если задан положительный TTL — ключ удалится автоматически по истечении этого времени
            self.connections[db].expire(key, period)

    @lazy_connect(CACHE_DB)
    def cache_get(self, key) -> str | None:
        """Получает значение из локального кэша (база данных 0).

        Если Redis недоступен — возвращает None.
        """
        try:
            value = self.get(key=key, db=CACHE_DB)
        except ConnectionError:
            value = None
        return value

    @lazy_connect(CACHE_DB)
    def cache_set(self, key, value, period) -> None:
        """Сохраняет значение в локальном кэше.
        
        Если соединение с Redis прерывается — просто пропускаем (кэш не критичен).
        """
        with contextlib.suppress(ConnectionError):
            self.set(key, value, period, db=CACHE_DB)

cache = Cache(  host = config.REDIS_URL,
                port = config.REDIS_PORT,
                username = config.REDIS_USER,
                password = config.REDIS_USER_PASSWORD)