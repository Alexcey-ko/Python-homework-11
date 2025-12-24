"""Приложение для бронирования авиабилетов."""

import asyncio

from app.client import Client


async def main():
    """Точка входа в приложение."""
    try:
        #Запуск приложения
        async with Client() as client:
            await client.run()
    except KeyboardInterrupt:
        print('Операция прервана пользователем.')

asyncio.run(main())