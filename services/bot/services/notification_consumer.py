import asyncio
import json
import logging
import aio_pika

from config import RabbitMQConfig
from schemas.notification import BotMessage

logger = logging.getLogger(__name__)

class Consumer:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self.exchange: aio_pika.Exchange = None
        self.notification_queue: aio_pika.Queue = None
        self._running = False

    async def connect(self):
        if self.connection:
            return
        
        self.connection = await aio_pika.connect_robust(self.config.amqp_url)
        self.channel = await self.connection.channel()

        await self.channel.set_qos(prefetch_count=self.config.prefetch_count)
        
        self.exchange = await self.channel.declare_exchange(
            name=self.config.notifications_exchange,
            type=self.config.notifications_exchange_type,
            durable=True
        )

        self.notification_queue = await self.channel.declare_queue(self.config.bot_notifications_queue, durable=True)
        await self.notification_queue.bind(self.exchange)

    async def start_consuming(self):
        if not self.connection:
            await self.connect()

        try:
            await self.notification_queue.consume(self.handle_notification)
        except Exception as e:
            logger.error(f"Ошибка начала потребления: {e}")

    async def handle_notification(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                data = json.loads(message.body)

                notification = BotMessage.model_validate(data)

                from main import bot
                await bot.send_message(notification.chat_id, notification.message)

            except Exception as e:
                logger.error(f"Ошибка при получении уведомления: {e}")

    async def disconnect(self):
        self._running = False
        
        if self.connection:
            self.connection.close()

    async def run(self):
        try:
            await self.connect()
            await self.start_consuming()
            self._running = True

            while self._running:
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            logger.info("Получен сигнал остановки")
        finally:
            await self.disconnect()

consumer = Consumer(RabbitMQConfig())