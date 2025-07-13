from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class LeadBase(BaseModel):
    full_name: str
    contact_phone: str
    contact_email: Optional[str] = None
    service_type: str
    preferred_date: datetime
    comment: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
