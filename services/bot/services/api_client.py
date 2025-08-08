from http import HTTPStatus
import httpx
from pydantic.type_adapter import TypeAdapter
from config import settings
from schemas.auth import AuthResponce, LoginRequest, RegisterRequest, TokenPair, UserData, UserResponce
from schemas.lead import LeadCreate, LeadResponce
from redis_utils.tokens import save_token, get_token
from utils.exceptions import TokenNotFoundError

def get_auth_headers(token: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

async def get_access_token(tg_id: int) -> str:
    access_token = await get_token('access_token', tg_id)

    if access_token:
        return access_token
    
    refresh_token = await get_token('refresh_token', tg_id)

    if not refresh_token:
        raise TokenNotFoundError
    
    tokens = await refresh_token_pair(tg_id, refresh_token)

    return tokens.access_token

async def register_user(data: RegisterRequest) -> UserResponce:
    async with httpx.AsyncClient() as client:
        auth_data = {
            "login": data.login,
            "password": data.password
        }

        auth_responce = await client.post(
            f"{settings.auth_service_url}/register",
            json=auth_data
        )

        auth_responce.raise_for_status()
        auth_result = AuthResponce.model_validate(auth_responce.json())

        await save_token('access_token', data.telegram_id, auth_result.token_pair.access_token)
        await save_token('refresh_token', data.telegram_id, auth_result.token_pair.refresh_token)

        user_data = {
            "telegram_id": data.telegram_id,
            "full_name": data.full_name,
            "contact_phone": data.contact_phone
        }

        user_responce = await client.post(
            f"{settings.users_service_url}/profile",
            json=user_data,
            headers=get_auth_headers(auth_result.token_pair.access_token)
        )

        user_responce.raise_for_status()
        user_result = user_responce.json()

        from .user_cache import cache_user_data
        await cache_user_data(data.telegram_id, UserData.model_validate(user_result))

        responce = UserResponce(
            id = user_result["id"],
            auth_id=auth_result.id,
            login=auth_result.login,
            token_pair=auth_result.token_pair,
            full_name=user_result["full_name"],
            contact_phone=user_data["contact_phone"]
        )

        return responce
    
async def login_user(data: LoginRequest) -> UserResponce | None:
    async with httpx.AsyncClient() as client:
        login_data = {
            "login": data.login,
            "password": data.password
        }

        auth_responce = await client.post(
            f"{settings.auth_service_url}/login",
            json=login_data
        )

        if not auth_responce:
            return None

        auth_result = AuthResponce.model_validate(auth_responce.json())

        await save_token('access_token', data.telegram_id, auth_result.token_pair.access_token)
        await save_token('refresh_token', data.telegram_id, auth_result.token_pair.refresh_token)
        
        user_responce = await client.get(
            f"{settings.users_service_url}/profile",
            headers=get_auth_headers(auth_result.token_pair.access_token)
        )

        user_responce.raise_for_status()
        user_result = user_responce.json()

        from .user_cache import cache_user_data
        await cache_user_data(data.telegram_id, UserData.model_validate(user_result))

        responce = UserResponce(
            id = user_result["id"],
            auth_id=auth_result.id,
            login=auth_result.login,
            token_pair=auth_result.token_pair,
            full_name=user_result["full_name"],
            contact_phone=user_result["contact_phone"]
        )

        return responce
    
async def create_lead(tg_id: int, data: LeadCreate) -> bool:
    async with httpx.AsyncClient() as client:
        json = data.model_dump(mode="json")

        responce = await client.post(
            f"{settings.leads_service_url}/",
            json=json
        )
        
        try:
            responce.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(e.response.text)

        if responce.status_code == HTTPStatus.CREATED:
            await get_leads(tg_id)
            return True
        
        return False

async def get_leads(tg_id: int) -> list[LeadResponce] | None:
    try:
        access_token = await get_access_token(tg_id)
        async with httpx.AsyncClient() as client:
            from .user_cache import get_user_data_cached
            user_data = await get_user_data_cached(tg_id)
            user_id = user_data.id
            

            responce = await client.get(
                f"{settings.leads_service_url}/user/{user_id}",
                headers=get_auth_headers(access_token)
            )

            if responce.status_code == HTTPStatus.NOT_FOUND:
                return None
            
            adapter = TypeAdapter(list[LeadResponce])
            leads: list[LeadResponce] = adapter.validate_python(responce.json())
            
            from .user_cache import cache_leads
            await cache_leads(tg_id, leads)

            return leads
    except TokenNotFoundError:
        raise
    
async def get_user_data(tg_id: int) -> UserData:
    try:
        access_token = await get_access_token(tg_id)

        async with httpx.AsyncClient() as client:

            responce = await client.get(
                f"{settings.users_service_url}/profile",
                headers=get_auth_headers(access_token)
            )
            responce.raise_for_status()
            
            user_data = UserData.model_validate(responce.json())
            
            from .user_cache import cache_user_data
            await cache_user_data(tg_id, user_data)
            return user_data
    except TokenNotFoundError:
        raise
    
async def refresh_token_pair(tg_id: int, refresh_token: str) -> TokenPair:
    async with httpx.AsyncClient() as client:
        responce = await client.post(
            f"{settings.auth_service_url}/refresh",
            json={ "refresh_token": refresh_token }
        )

        responce.raise_for_status()
        if tokens := TokenPair.model_validate(responce.json()):
            await save_token('access_token', tg_id, tokens.access_token)
            await save_token('refresh_token', tg_id, tokens.refresh_token)
        return tokens