from http import HTTPStatus
import httpx
from config import settings
from schemas.auth import AuthResponce, RegisterRequest, UserResponce
from schemas.lead import LeadCreate

def get_auth_headers(token: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

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

        responce = UserResponce(
            id=auth_result.id,
            login=auth_result.login,
            token_pair=auth_result.token_pair,
            full_name=user_result["full_name"],
            contact_phone=user_data["contact_phone"]
        )

        return responce
    
async def login_user(data: dict) -> UserResponce:
    async with httpx.AsyncClient() as client:
        login_data = {
            "login": data.get("login"),
            "password": data.get("password")
        }

        responce = await client.post(
            f"{settings.auth_service_url}/login",
            json=login_data
        )
        responce.raise_for_status()
        return responce.json()
    
async def create_lead(data: LeadCreate) -> bool:
    async with httpx.AsyncClient() as client:
        json = data.model_dump_json()

        responce = await client.post(
            f"{settings.leads_service_url}/",
            json=json
        )

        if responce.status_code == HTTPStatus.CREATED:
             return True
        
        return False