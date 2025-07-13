from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ManagerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    login: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_admin: bool = False

class ManagerCreate(ManagerBase):
    password: str = Field(..., min_length=6, max_length=100)

class ManagerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)

class ManagerResponse(ManagerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ManagerLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    login: Optional[str] = None