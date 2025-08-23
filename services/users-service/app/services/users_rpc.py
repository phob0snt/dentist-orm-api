import asyncio
import logging
from typing import Any, Dict
import aio_pika
from aio_pika.patterns import RPC

from app.schemas.user import UserCreate, UserResponce
from .user import create_user_data, get_tg_by_user_id, get_user_data
from app.config import RabbitMQConfig
from app.db.session import SessionLocal
from app.core.security import verify_token

logger = logging.getLogger(__name__)

class UsersRpc:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self.rpc: aio_pika.patterns.RPC = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.config.amqp_url)
            self.channel = await self.connection.channel()
            self.rpc = await RPC.create(self.channel)

            await self.rpc.register("users.create", self.handle_creation, auto_delete=True)
            await self.rpc.register("users.get", self.handle_get, auto_delete=True)
            await self.rpc.register("users.get_tg_by_user_id", self.handle_tg_get, auto_delete=True)

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
            
            payload = verify_token(token)

            request = UserCreate.model_validate(kwargs.get("data"))

            result = create_user_data(
                user=request,
                auth_id=payload.get("auth_id"),
                db=db
            )

            responce = UserResponce.model_validate(result)

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

    async def handle_get(self, **kwargs) -> Dict[str, Any]:
        db = SessionLocal()

        try:
            token = kwargs.get("token")

            if not token:
                return {"error": "Отсутствует токен"}
            
            payload = verify_token(token)

            result = get_user_data(
                token_payload=payload,
                db=db
            )

            responce = UserResponce.model_validate(result)

            return responce.model_dump()
        
        except ValueError as e:
            error = f"Ошибка валидации данных: {str(e)}"
            logger.error(error)
            return {"error": error}
        except Exception as e:
            error = f"Ошибка получения данных пользователя: {str(e)}"
            logger.error(error)
            return {"error": error}
        finally:
            db.close()

    async def handle_tg_get(self, **kwargs) -> int:
        logger.info("Users RPC вызвал handle_tg")

        db = SessionLocal()

        try:
            user_id = kwargs.get("user_id")
            logger.info(f"User id: {user_id}")
            result = get_tg_by_user_id(user_id=user_id, db=db)
            logger.info(f"Got TG id: {result}")
            
            return result
        
        except ValueError as e:
            error = f"Ошибка валидации данных: {str(e)}"
            logger.error(error)
            return {"error": error}
        except Exception as e:
            error = f"Ошибка получения данных пользователя: {str(e)}"
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

users_rpc = UsersRpc(RabbitMQConfig())