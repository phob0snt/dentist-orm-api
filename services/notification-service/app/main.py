import asyncio
import logging
import sys

from consumer import consumer
from producer import producer
from rpc_client import rpc_client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
async def main():
    logger.info(" === Запуск Notification Service ===")
    
    try:
        await producer.connect()
        await rpc_client.connect()

        consumer_task = asyncio.create_task(consumer.run())
        
        await consumer_task
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise
    finally:
        logger.info("Завершение работы...")
        
        await consumer.stop()
        
        await producer.disconnect()
        
        logger.info(" === Notification Service остановлен ===")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        sys.exit(1)