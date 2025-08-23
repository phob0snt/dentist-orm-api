import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from config import settings
from redis_utils.tokens import init_cache as init_token_cache
from redis_utils.cache import init_cache as init_user_cache
from redis_utils.fsm import create_fsm_storage
from handlers import all_routers
from services.rpc_client import rpc_client
from services.notification_consumer import consumer

import logging
bot = Bot(token=settings.bot_token)

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("запуск ботика)")


    logger.info("🔄 Инициализация Redis...")
    await init_token_cache(settings.redis_host, settings.redis_port)
    await init_user_cache(settings.redis_host, settings.redis_port)
    redis_storage = await create_fsm_storage(settings.redis_host, settings.redis_port)
    logger.info("✅ Redis подключен")

    dp = Dispatcher(storage=redis_storage)

    consumer_task = asyncio.create_task(consumer.run())

    await rpc_client.connect()

    logger.info(f"📋 Найдено роутеров: {len(all_routers)}")
    
    for router in all_routers:        
        dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        consumer_task.cancel()
    

if __name__ == "__main__":
    asyncio.run(main())