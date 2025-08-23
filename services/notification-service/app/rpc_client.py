import logging
import sys
import aio_pika
from config import RabbitMQConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RpcClient:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self.rpc: aio_pika.patterns.RPC = None

    async def connect(self):
        if self.connection:
            return
        try:
            self.connection = await aio_pika.connect_robust(self.config.amqp_url)
            self.channel = await self.connection.channel()
            self.rpc = await aio_pika.patterns.RPC.create(self.channel)
            logger.info("RPC клиент подключен")
        except Exception as e:
            logger.error("Ошибка подключения RPC")
            raise

    async def call_users_service(self, method: str, data: dict):
        if not self.connection:
            return
        try:
            rpc_method = f"users.{method}"
            logger.info(f"Отправка RPC запроса {rpc_method}")
            result = await self.rpc.call(rpc_method, data)
            logger.info(f"Получен RPC Ответ: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка при вызове users service: {e}")

rpc_client = RpcClient(RabbitMQConfig())