import logging
from typing import Optional
from redis.asyncio import Redis

from schemas.lead import LeadResponce

logger = logging.getLogger(__name__)

redis_user_cache: Optional[Redis] = None

async def init_cache(host: str, port: int):
    global redis_user_cache
    try:
        logger.info(f"🔄 Инициализация Redis user cache: {host}:{port}/db2")
        
        # ✅ Создаем Redis клиент
        redis_user_cache = Redis(
            host=host, 
            port=port, 
            db=2, 
            decode_responses=True,
            socket_connect_timeout=10,
            socket_timeout=10
        )
        
        # ✅ ОБЯЗАТЕЛЬНО: проверяем подключение
        await redis_user_cache.ping()
        
        # ✅ Проверяем что переменная установлена
        if redis_user_cache is None:
            raise RuntimeError("redis_user_cache остался None после инициализации")
            
        logger.info(f"✅ Redis user cache успешно инициализирован: {redis_user_cache}")
        logger.info(f"   Тип: {type(redis_user_cache)}")
        logger.info(f"   Подключение: {host}:{port}/db2")
        
        # ✅ Тестируем операцию
        test_key = "init_test"
        await redis_user_cache.set(test_key, "test_value", ex=10)
        test_result = await redis_user_cache.get(test_key)
        await redis_user_cache.delete(test_key)
        
        if test_result == "test_value":
            logger.info("✅ Тест операций Redis прошел успешно")
        else:
            logger.error(f"❌ Тест операций не прошел: {test_result}")
            
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации Redis user cache: {e}")
        redis_user_cache = None
        import traceback
        traceback.print_exc()
        raise