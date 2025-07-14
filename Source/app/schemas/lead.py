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

class LeadStatusUpdate(BaseModel):
    status: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "contacted"
            }
        }

class Lead(LeadBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
