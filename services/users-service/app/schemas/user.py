from pydantic import BaseModel

class User(BaseModel):
    auth_id: str
    full_name: str
    contact_phone: str
    telegram_id: str