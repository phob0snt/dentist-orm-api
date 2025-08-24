import asyncio
import datetime
import json
import logging
import aio_pika

from schemas.notification import LeadNotification
from config import RabbitMQConfig
from producer import producer
from rpc_client import rpc_client

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Consumer:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self.exchange: aio_pika.Exchange = None
        self.lead_queue: aio_pika.Queue = None

    async def connect(self):
        if self.connection:
            return
        
        try:
            self.connection = await aio_pika.connect_robust(self.config.amqp_url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=self.config.prefetch_count)

            self.lead_queue = await self.channel.declare_queue(
                self.config.notification_lead_queue, 
                durable=True
            )

            logger.info("Consumer подключен к RabbitMQ")
            
        except Exception as e:
            logger.error(f"Ошибка подключения: {e}")
            raise
    
    async def handle_message(self, message: aio_pika.IncomingMessage):
        try:
            body = message.body.decode('utf-8')
            logger.info(f"Получено сообщение: {body}")
            
            data = json.loads(body)
            notification = LeadNotification.model_validate(data)

            if not notification.appointment_date and not notification.status:
                logger.info("Поступило пустое уведомление, отправка отменена")
                return

            chat_id = await rpc_client.call_users_service(
                method="get_tg_by_user_id",
                data={
                    "user_id": notification.user_id
                }
            )
            status_notification = ""
            date_notification = ""
            if notification.status:
                from utils.status import status
                if notification.status not in status.keys():
                    logger.info("Неизвестный статус, отмена отправки уведомления")
                    return
                
                status_notification = (f"🔔 Статус вашей записи \#{notification.lead_id} "
                                   f"изменён на *{status[notification.status]}*\n\n")
            if notification.appointment_date:
                date = datetime.datetime.fromisoformat(notification.appointment_date)
                str_date = date.strftime('%d.%m в %H:%M').replace(".", "\\.")
                date_notification = (f"🕒 Вы записаны\. Время записи: __{str_date}__")

            bot_message = {
                "chat_id": int(chat_id),
                "message": status_notification + date_notification
            }

            logger.info(f"Отправка уведомления: {bot_message}")
            await producer.publish(bot_message)
            await message.ack()
            logger.info("Уведомление отправлено")
            
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {e}")
    
    async def start_consuming(self):
        if not self.connection:
            await self.connect()
        
        try:
            await self.lead_queue.consume(self.handle_message)
            
        except Exception as e:
            logger.error(f"Ошибка запуска потребления: {e}")
            raise
    async def disconnect(self):
        if self.connection:
            self.connection.close()

    async def run(self):
        try:
            logger.info("Запуск consumer...")
            
            await self.connect()
            
            await self.start_consuming()
            
            self._running = True
            logger.info("Consumer работает, ожидание сообщений...")
            
            while self._running:
                await asyncio.sleep(1)
                
        except asyncio.CancelledError:
            logger.info("Получен сигнал остановки")
        except Exception as e:
            logger.error(f"Критическая ошибка в consumer: {e}")
            raise
        finally:
            await self.disconnect()

    async def stop(self):
        logger.info("Остановка consumer...")
        self._running = False
        

consumer = Consumer(RabbitMQConfig())