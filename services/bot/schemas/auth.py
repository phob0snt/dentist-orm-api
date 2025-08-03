from typing import Optional
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=64, description="Имя")
    contact_phone: str = Field(..., min_length=10, max_length=20, description="Номер телефона")
    login: str = Field(..., min_length=6, max_length=32, description="Логин")
    password: str = Field(..., min_length=6, max_length=32, description="Пароль")
    telegram_id: str = Field(..., description="Telegram ID")

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Иван Иванов",
                "contact_phone": "+7 900 123-45-67",
                "login": "ivan_ivanov",
                "password": "secure123",
                "telegram_id": "123456789"
            }
        }

class LoginRequest(BaseModel):
    login: str = Field(..., min_length=6, description="Логин")
    password: str = Field(..., min_length=6, description="Пароль")

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AuthResponce(BaseModel):
    id: int
    login: str
    token_pair: TokenPair

class UserData(BaseModel):
    id: int
    full_name: str
    contact_phone: str

class UserResponce(BaseModel):
    id: int
    auth_id: int
    login: str
    token_pair: TokenPair
    full_name: str
    contact_phone: str