from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage


async def create_fsm_storage(host: str, port: int):
    redis = Redis(host=host, port=port, decode_responses=True, db=0)
    return RedisStorage(redis)