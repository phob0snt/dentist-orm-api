from pydantic import TypeAdapter
from schemas.lead import LeadCreate, LeadResponce
from services.auth_rpc import get_access_token
from utils.exceptions import TokenNotFoundError
from services.rpc_client import rpc_client


async def create_lead(tg_id: int, data: LeadCreate) -> bool:
    responce = await rpc_client.call_lead_service(
        method="create",
        data={
            "data": data.model_dump()
        }
    )

    if responce.get("id"):
        await get_leads(tg_id)
        return True
    
    return False

async def get_leads(tg_id: int) -> list[LeadResponce] | None:
    try:
        access_token = await get_access_token(tg_id)

        from .user_cache import get_user_data_cached
        user_data = await get_user_data_cached(tg_id, True)
        user_id = user_data.id
        

        responce = await rpc_client.call_lead_service(
            method="get_for_user",
            data={
                "user_id": user_id,
                "token": access_token
            }
        )

        if not responce:
            return
        
        adapter = TypeAdapter(list[LeadResponce])
        leads: list[LeadResponce] = adapter.validate_python(responce)
        
        from .user_cache import cache_leads
        await cache_leads(tg_id, leads)

        return leads
    except TokenNotFoundError:
        raise