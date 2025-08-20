import asyncio
import logging
import os
from dotenv import load_dotenv
from typing import Any, Dict
import aio_pika
from aio_pika.patterns import RPC

from app.schemas.lead import LeadCreate, Lead
from .lead import create_lead, get_leads_by_user_id
from app.db.session import SessionLocal
from app.core.security import verify_token

logger = logging.getLogger(__name__)

class UsersConsumer:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None
        self.rpc = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
            self.rpc = await RPC.create(self.channel)

            await self.rpc.register("lead.create", self.handle_creation, auto_delete=True)
            await self.rpc.register("lead.get_for_user", self.handle_get_for_user, auto_delete=True)

            logger.info("Auth RPC Consumer подключен")

        except Exception as e:
            logger.error(f"Ошибка подключения к RabbitMQ: {e}")
            raise

    async def handle_creation(self, **kwargs) -> Dict[str, Any]:
        db = SessionLocal()

        try:
            token = kwargs.get("token")

            if not token:
                return {"error": "Отсутствует токен"}
            
            verify_token(token)

            request = LeadCreate.model_validate(kwargs.get("data"))

            result = create_lead(
                lead_data=request,
                db=db
            )

            responce = Lead.model_validate(result)

            return responce.model_dump()
        
        except ValueError as e:
            error = f"Ошибка валидации данных: {str(e)}"
            logger.error(error)
            return {"error": error}
        except Exception as e:
            error = f"Ошибка регистрации: {str(e)}"
            logger.error(error)
            return {"error": error}
        finally:
            db.close()

    async def handle_get_for_user(self, **kwargs) -> Dict[str, Any]:
        db = SessionLocal()

        try:
            token = kwargs.get("token")
            user_id = kwargs.get("user_id")

            if not token:
                return {"error": "Отсутствует токен"}
            
            if not user_id:
                return {"error": "Отсутствует user_id"}
            
            verify_token(token)

            result = get_leads_by_user_id(
                user_id=user_id,
                db=db
            )

            responce = Lead.model_validate(result)

            return responce.model_dump()
        
        except ValueError as e:
            error = f"Ошибка валидации данных: {str(e)}"
            logger.error(error)
            return {"error": error}
        except Exception as e:
            error = f"Ошибка регистрации: {str(e)}"
            logger.error(error)
            return {"error": error}
        finally:
            db.close()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            logger.info("Auth consumer отключен")

    async def run(self):
        await self.connect()

        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("Получен сигнал остановки")
        finally:
            await self.disconnect()

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

users_consumer = UsersConsumer(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/")