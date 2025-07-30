from pydantic import BaseModel

class UserBase(BaseModel):
    telegram_id: str
    full_name: str
    contact_phone: str

class UserCreate(UserBase):
    pass

class UserResponce(UserBase):
    id: int
    auth_id: int

    class Config:
        from_attributes = True