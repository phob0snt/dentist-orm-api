import json
from schemas.lead import LeadResponce
from schemas.auth import UserData
from .api_client import get_leads, get_user_data
from redis_utils.config import redis_ttl_config

async def get_leads_cached(tg_id: int) -> list[LeadResponce]:
    key = f"{tg_id}:leads"
    from redis_utils.cache import redis_user_cache
    cached_leads = await redis_user_cache.get(key)

    if cached_leads:
        if leads := json.loads(cached_leads):
            return [LeadResponce(**lead) for lead in leads]
    
    return await get_leads(tg_id)

async def get_user_data_cached(tg_id: int) -> UserData:
    key = f"{tg_id}:profile"
    from redis_utils.cache import redis_user_cache
    cached_profile = await redis_user_cache.get(key)

    if user_data := UserData.model_validate(json.loads(cached_profile)):
        return user_data
    
    return await get_user_data(tg_id)

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