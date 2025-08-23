from dataclasses import dataclass
import os
import aio_pika
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

AUTH_HOST = os.getenv("AUTH_SERVICE_HOST")
AUTH_PORT = os.getenv("AUTH_SERVICE_PORT")

USERS_HOST = os.getenv("USERS_SERVICE_HOST")
USERS_PORT = os.getenv("USERS_SERVICE_PORT")

LEAD_HOST = os.getenv("LEAD_SERVICE_HOST")
LEAD_PORT = os.getenv("LEAD_SERVICE_PORT")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

class Settings(BaseModel):
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: str = os.getenv("REDIS_PORT")

    bot_token: str = os.getenv("BOT_TOKEN")

    jwt_secret: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")


    auth_service_url: str = f"http://{AUTH_HOST}:{AUTH_PORT}/api"


    users_service_url: str = f"http://{USERS_HOST}:{USERS_PORT}/api"


    lead_service_url: str = f"http://{LEAD_HOST}:{LEAD_PORT}/api/leads"

    rabbitmq_url: str = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"

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

settings = Settings()