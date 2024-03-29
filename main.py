import asyncio
from aiogram import Bot, Dispatcher
import logging

from handlers.chat import chat_router
from handlers.basic import basic_router
from middlewares.db_middleware import DataBaseMiddelware

from sql.db import create_pool

from config import settings


session_factory = create_pool(settings.db_url)

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.update.outer_middleware(DataBaseMiddelware(session_factory))
    dp.include_router(basic_router)
    dp.include_router(chat_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
