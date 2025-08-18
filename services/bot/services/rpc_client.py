import logging
from typing import Optional
import aio_pika
from aio_pika.patterns import RPC

logger = logging.getLogger(__name__)

class RpcClient:
    def __init__(self, amqp_url):
        self.amqp_url = amqp_url
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.rpc: Optional[RPC] = None
        self._connected = False

    async def connect(self):
        if self._connected:
            return
        try:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
            self.rpc = await RPC.create(self.channel)
            self._connected = True
            logger.info("RPC клиент подключен")
        except Exception as e:
            logger.error("Ошибка подключения RPC")
            self._connected = False
            raise


    async def call_auth_service(self, method: str, data: dict) -> dict:
        if not self._connected:
            raise RuntimeError("RPC клиент не подключен")
        
        try:
            result = await self.rpc.call(f"auth.{method}", data)
            return result
        except Exception as e:
            logger.error(f"Ошибка вызова auth сервиса: {e}")

    async def call_users_service(self, method: str, data: dict) -> dict:
        if not self._connected:
            raise RuntimeError("RPC клиент не подключен")
        
        try:
            result = await self.rpc.call(f"users.{method}", data)
            return result
        except Exception as e:
            logger.error(f"Ошибка вызова users сервиса: {e}")

import config

rpc_client = RpcClient(config.settings.rabbitmq_url)