import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from settings import BOT_TOKEN
from core.routers import routers

async def main():
    try:
        logging.basicConfig(level=logging.INFO)
        storage = MemoryStorage()
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
        dp = Dispatcher(bot=bot, storage=storage)
        dp.include_routers(*routers)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        raise

def start_app():
    asyncio.run(main())

if __name__ == "__main__":
    start_app()