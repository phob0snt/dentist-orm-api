from schemas.auth import UserData
from services.auth_rpc import get_access_token
from utils.exceptions import TokenNotFoundError
from services.rpc_client import rpc_client


async def get_user_data(tg_id: int) -> UserData:
    try:
        access_token = await get_access_token(tg_id)


        responce = await rpc_client.call_users_service(
            method="get",
            data={
                "token": access_token
            }
        )
        
        user_data = UserData.model_validate(responce)
        
        from .user_cache import cache_user_data
        await cache_user_data(tg_id, user_data)
        return user_data
    except TokenNotFoundError:
        raise