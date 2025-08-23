import json
import logging
import aio_pika

from app.config import RabbitMQConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class NotificaionProducer:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self.queue: aio_pika.Queue = None
    
    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.config.amqp_url)
            self.channel = await self.connection.channel()

            await self.channel.set_qos(prefetch_count=self.config.prefetch_count)
        except Exception as e:
            logger.error(f"Ошибка при подключении: {e}")
    
    async def publish(self, data: str):
        if not self.connection:
            await self.connect()
        
        logger.info("publishing")
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(data).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=self.config.notification_lead_queue
        )
        logger.info("published")

    async def disconnect(self):
        if self.connection:
            self.connection.close()

producer = NotificaionProducer(RabbitMQConfig())