from enum import Enum
from pydantic import BaseModel, Field

class AccountRole(str, Enum):
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"

class AccountCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class AccountLogin(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class AccountResponce(BaseModel):
    id: int
    login: str
    role: AccountRole
    is_active: bool
    token_pair: TokenPair

    class Config:
        orm_mode = True