import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from typing import Any, Dict
import aio_pika
from aio_pika.patterns import RPC

from app.schemas.auth import AccountCreate, AccountLogin, AccountRole, RefreshRequest
from .auth import authenticate_user, refresh_token_pair, register_user_with_login
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AuthConsumer:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None
        self.rpc: RPC = None
    
    async def connect(self, retries: int = 3):
        for attempt in range(retries):
            try:
                self.connection = await aio_pika.connect_robust(self.amqp_url)
                self.channel = await self.connection.channel()
                self.rpc = await RPC.create(self.channel)

                await self.rpc.register("auth.register_user", self.handle_register, auto_delete=True)
                await self.rpc.register("auth.login", self.handle_login, auto_delete=True)
                await self.rpc.register("auth.refresh", self.handle_refresh, auto_delete=True)

                logger.info("Auth RPC Consumer подключен")

            except Exception as e:
                logger.error(f"Ошибка подключения к RabbitMQ: {e}")

                if attempt < retries - 1:
                    delay = 5
                    logger.info(f"Попытка переподключения через {delay} секунд. Осталось попыток: {retries - attempt - 1}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Невозможно подключиться к RabbitMQ: {e}. Остановка сервиса.")
                    sys.exit(1)
                raise

    async def handle_register(self, **kwargs) -> Dict[str, Any]:
        db = SessionLocal()

        try:
            logger.error(f"получены данные: {kwargs}")
            request = AccountCreate.model_validate(kwargs.get("data"))

            result = register_user_with_login(
                register_data=request,
                role=AccountRole.USER,
                db=db
            )

            # responce = AccountResponce.model_validate(result)

            return {
                "id": result.id,
                "login": result.login,
                "role": str(result.role.value),
                "is_active": result.is_active,
                "token_pair": {
                    "access_token": result.token_pair.access_token,
                    "refresh_token": result.token_pair.refresh_token,
                    "token_type": result.token_pair.token_type
                }
            }
        
        except ValueError as e:
            error = f"Ошибка валидации данных: {e}"
            logger.error(error)
            return {"error": error}
        except Exception as e:
            error = f"Ошибка регистрации: {e}"
            logger.error(error)
            return {"error": error}
        finally:
            db.close()

    async def handle_login(self, **kwargs) -> Dict[str, Any]:
        db = SessionLocal()

        try:
            request = AccountLogin.model_validate(kwargs.get("data"))

            result = authenticate_user(
                login_data=request,
                db=db
            )

            # responce = AccountResponce.model_validate(result)

            return {
                "id": result.id,
                "login": result.login,
                "role": str(result.role.value),
                "is_active": result.is_active,
                "token_pair": {
                    "access_token": result.token_pair.access_token,
                    "refresh_token": result.token_pair.refresh_token,
                    "token_type": result.token_pair.token_type
                }
            }
        
        except ValueError as e:
            error = f"Ошибка валидации данных: {str(e)}"
            logger.error(error)
            return {"error": error}
        except Exception as e:
            error = f"Ошибка входа: {str(e)}"
            logger.error(error)
            return {"error": error}
        finally:
            db.close()

    async def handle_refresh(self, **kwargs) -> Dict[str, Any]:
        db = SessionLocal()

        try:
            token = kwargs.get("refresh_token")

            if not token:
                return { "error": "Refresh токен не предоставлен"}

            result = refresh_token_pair(
                refresh_token=RefreshRequest(refresh_token=token),
                db=db
            )

            # responce = AccountResponce.model_validate(result)

            return {
                "token_pair": {
                    "access_token": result.access_token,
                    "refresh_token": result.refresh_token,
                    "token_type": result.token_type
                }
            }
        
        except Exception as e:
            error = f"Ошибка обновления токенов: {str(e)}"
            logger.error(error)
            return {"error": error}
        finally:
            db.close()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            logger.info("Auth consumer отключен")

    async def run(self):
        await self.connect(3)

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

auth_consumer = AuthConsumer(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/")