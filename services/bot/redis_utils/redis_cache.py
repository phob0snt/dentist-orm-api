from datetime import datetime, timezone
from typing import Literal
from redis.asyncio import Redis

from services.jwt_decoder import get_token_payload

redis_cache: Redis | None = None

async def init_cache(host: str, port: int):
    global redis_cache
    redis_cache = Redis(host=host, port=port, db=1)

async def save_token(type: Literal["refresh_token", "access_token"], tg_id: int, token: str):
    payload = get_token_payload(token=token)

    if not payload:
        print("Неверный токен")

    ttl_datetime = datetime(payload.get("exp"))
    now = datetime.now(timezone.utc)
    ttl_seconds = int((ttl_datetime - now).total_seconds)

    await redis_cache.set(f"{type}:{tg_id}", token, ex=ttl_seconds)

async def get_token(type: Literal["refresh_token", "access_token"], tg_id: int) -> str:
    token = await redis_cache.get(f"{type}:{tg_id}")

    if not token:
        print(f"Токен пользователя {tg_id} не найден")

    return token