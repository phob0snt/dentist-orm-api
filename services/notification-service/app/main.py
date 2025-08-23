import asyncio
import logging
import os
import sys

from consumer import consumer
from producer import producer
from rpc_client import rpc_client

# Настроить логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
async def main():
    logger.info("🚀 === Запуск Notification Service ===")
    
    try:
        # Подключить producer
        logger.info("🔄 Подключение producer...")
        await producer.connect()
        logger.info("✅ Producer подключен")
        await rpc_client.connect()
        logger.info("✅ RPC Client подключен")
        
        # Запустить consumer в фоновой задаче
        logger.info("🔄 Запуск consumer...")
        consumer_task = asyncio.create_task(consumer.run())
        logger.info("✅ Consumer задача создана")
        
        # Ждать завершения consumer
        await consumer_task
        
    except KeyboardInterrupt:
        logger.info("🛑 Получен SIGINT")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise
    finally:
        logger.info("🔄 Завершение работы...")
        
        # Остановить consumer
        await consumer.stop()
        
        # Отключить producer
        await producer.disconnect()
        
        logger.info("🏁 === Notification Service остановлен ===")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"💥 Фатальная ошибка: {e}")
        sys.exit(1)