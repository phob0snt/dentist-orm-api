import logging
from schemas.auth import UserData
from services.auth_rpc import get_access_token
from utils.exceptions import TokenNotFoundError
from services.rpc_client import rpc_client

logger = logging.getLogger(__name__)

async def get_user_data(tg_id: int) -> UserData:
    try:
        access_token = await get_access_token(tg_id)


        responce = await rpc_client.call_users_service(
            method="get",
            data={
                "token": access_token
            }
        )

        try:
            user_data = UserData.model_validate(responce)
        except Exception as e:
            logger.error(f"Ошибка валидации данных: {e}")
            return
        
        from .user_cache import cache_user_data
        await cache_user_data(tg_id, user_data)
        return user_data
    except TokenNotFoundError:
        raise