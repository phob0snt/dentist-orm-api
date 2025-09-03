import logging
from schemas.auth import AuthResponce, LoginRequest, RegisterRequest, TokenPair, UserData, UserResponce
from redis_utils.tokens import get_token, save_token
from utils.exceptions import TokenNotFoundError
from .rpc_client import rpc_client

logger = logging.getLogger(__name__)
async def register_user(data: RegisterRequest) -> UserResponce | None:
    try:
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
    except Exception as e:
        logger.error(f"Ошибка при регистрации: {e}")
        return None

async def login_user(data: LoginRequest) -> UserResponce | None:
    try:
        login_data = {
            "login": data.login,
            "password": data.password
        }

        auth_responce = await rpc_client.call_auth_service(
            method="login",
            data={
                "data": login_data
            }
        )

        if not auth_responce:
            logger.error("Ошибка получения данных авторизации")
            return None

        auth_result = AuthResponce.model_validate(auth_responce)

        await save_token('access_token', data.telegram_id, auth_result.token_pair.access_token)
        await save_token('refresh_token', data.telegram_id, auth_result.token_pair.refresh_token)
        
        from services.user_rpc import get_user_data

        user_responce = await get_user_data(data.telegram_id)

        if not user_responce:
            logger.error("Ошибка получения данных пользователя")
            return None

        from .user_cache import cache_user_data
        await cache_user_data(data.telegram_id, user_responce)

        responce = UserResponce(
            id = user_responce.id,
            auth_id=auth_result.id,
            login=auth_result.login,
            token_pair=auth_result.token_pair,
            full_name=user_responce.full_name,
            contact_phone=user_responce.contact_phone
        )

        return responce
    except Exception as e:
        logger.error(f"Ошибка при входе: {e}")

async def refresh_token_pair(tg_id: int, refresh_token: str) -> TokenPair:
    try:
        responce = await rpc_client.call_auth_service(
            method="refresh",
            data={
                "refresh_token": refresh_token
            }
        )

        if not responce or "token_pair" not in responce:
            logger.error("Не удалось обновить токены")
            return None
        
        tokens = TokenPair.model_validate(responce["token_pair"])

        await save_token('access_token', tg_id, tokens.access_token)
        await save_token('refresh_token', tg_id, tokens.refresh_token)

        return tokens
    except Exception as e:
        logger.error(f"Ошибка при обновлении токенов: {e}")
        return None

async def get_access_token(tg_id: int) -> str:
    access_token = await get_token('access_token', tg_id)

    if access_token:
        return access_token
    
    refresh_token = await get_token('refresh_token', tg_id)

    if not refresh_token:
        raise TokenNotFoundError
    
    tokens = await refresh_token_pair(tg_id, refresh_token)

    return tokens.access_token