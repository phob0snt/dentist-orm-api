import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from redis_utils.redis_cache import init_cache
from redis_utils.storage import create_fsm_storage

import logging

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("запуск ботика)")

    bot = Bot(token=settings.bot_token)

    redis_storage = await create_fsm_storage(settings.redis_host, settings.redis_port)
    await init_cache(settings.redis_host, settings.redis_port)

    dp = Dispatcher(storage=redis_storage)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())