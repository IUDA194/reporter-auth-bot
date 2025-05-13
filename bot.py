import asyncio
import logging
import sys

from dotenv import load_dotenv, find_dotenv
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.hendlers import (
    start_router,
)

logging.basicConfig(
    level=logging.INFO,  # Уровень логгирования
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[  # Обработчики логов (вывод в консоль и файл)
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler('logs.log')  # Логирование в файл
    ]
)

load_dotenv(find_dotenv())

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


async def main() -> None:
    
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))

    dp.include_router(start_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())