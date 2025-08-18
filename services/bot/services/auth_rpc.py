from schemas.auth import AuthResponce, RegisterRequest, UserData, UserResponce
from redis_utils.tokens import save_token
from services.api_client import get_auth_headers
from .rpc_client import rpc_client

async def register_user(data: RegisterRequest) -> UserResponce:
    auth_data = {
        "login": data.login,
        "password": data.password
    }

    auth_responce = await rpc_client.call_auth_service(
        method = "register_user",
        data = {
            "data": auth_data
        }
    )
    print(auth_responce)
    auth_result = AuthResponce.model_validate(auth_responce)

    await save_token('access_token', data.telegram_id, auth_result.token_pair.access_token)
    await save_token('refresh_token', data.telegram_id, auth_result.token_pair.refresh_token)

    user_data = {
        "telegram_id": data.telegram_id,
        "full_name": data.full_name,
        "contact_phone": data.contact_phone
    }

    user_responce = await rpc_client.call_users_service(
        method = "create",
        data = {
            "data": user_data,
            "token": auth_result.token_pair.access_token
        }
    )

    from .user_cache import cache_user_data
    await cache_user_data(data.telegram_id, UserData.model_validate(user_responce))

    responce = UserResponce(
        id = user_responce["id"],
        auth_id=auth_result.id,
        login=auth_result.login,
        token_pair=auth_result.token_pair,
        full_name=user_responce["full_name"],
        contact_phone=user_data["contact_phone"]
    )

    return responce