from dataclasses import dataclass
import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

@dataclass
class RabbitMQConfig:
    amqp_url: str = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"

    leads_exchange: str = "leads.events"
    leads_exchange_type: aio_pika.ExchangeType = aio_pika.ExchangeType.DIRECT
    notification_lead_queue: str = "notification.lead.events"

    notifications_exchange: str = "notifications.broadcast"
    notifications_exchange_type: aio_pika.ExchangeType = aio_pika.ExchangeType.FANOUT
    bot_notifications_queue: str = "bot.notifications"

    prefetch_count: int = 16