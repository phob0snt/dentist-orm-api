import json
import logging
from schemas.lead import LeadResponce
from schemas.auth import UserData
from .api_client import get_leads, get_user_data
from . import user_rpc
from . import lead_rpc
from redis_utils.config import redis_ttl_config

logger = logging.getLogger(__name__)

async def get_leads_cached(tg_id: int, fromRPC = False) -> list[LeadResponce]:
    key = f"{tg_id}:leads"
    from redis_utils.cache import redis_user_cache
    cached_leads = await redis_user_cache.get(key)

    if cached_leads:
        if leads := json.loads(cached_leads):
            return [LeadResponce(**lead) for lead in leads]
    if not fromRPC:
        return await get_leads(tg_id)
    else:
        return await lead_rpc.get_leads(tg_id)

async def get_user_data_cached(tg_id: int, fromRPC = False) -> UserData:
    key = f"{tg_id}:profile"
    from redis_utils.cache import redis_user_cache
    cached_profile = await redis_user_cache.get(key)

    if cached_profile:
        try:
            user_data = UserData.model_validate(json.loads(cached_profile))
            if user_data:
                return user_data
        except Exception as e:
            logger.error(f"Ошибка валидации UserData: {e}")
    
    if not fromRPC:
        return await get_user_data(tg_id)
    else:
        return await user_rpc.get_user_data(tg_id)

async def cache_leads(tg_id: int, leads: list[LeadResponce]):
    key = f"{tg_id}:leads"
    json_data = json.dumps([lead.model_dump() for lead in leads])
    from redis_utils.cache import redis_user_cache
    await redis_user_cache.set(key, json_data, ex=redis_ttl_config.leads_data)

async def cache_user_data(tg_id: int, data: UserData):
    key = f"{tg_id}:profile"
    json_data = json.dumps(data.model_dump())
    from redis_utils.cache import redis_user_cache
    await redis_user_cache.set(key, json_data, ex=redis_ttl_config.user_data)