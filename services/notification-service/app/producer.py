import json
import logging
import aio_pika

from config import RabbitMQConfig


BOT_QUEUE = "bot_queue"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Producer:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self.exchange: aio_pika.Exchange = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.config.amqp_url)
            self.channel = await self.connection.channel()

            await self.channel.set_qos(prefetch_count=self.config.prefetch_count)

            self.exchange = await self.channel.declare_exchange(
                name=self.config.notifications_exchange,
                type=self.config.notifications_exchange_type,
                durable=True
            )

            logger.info("Соединение установлено")
        except Exception as e:
            logger.error(f"Ошибка при установке соединения: {e}")

    async def publish(self, body: str):
        if not self.exchange:
            await self.connect()
        try:
            await self.exchange.publish(
                aio_pika.Message(
                    body=json.dumps(body).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=""
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")

    async def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("Соединение закрыто")

producer = Producer(RabbitMQConfig())