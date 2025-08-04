from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class LeadCreate(BaseModel):
    user_id: int
    service_type: str
    preferred_date: str
    comment: Optional[str] = None

class LeadResponce(LeadCreate):
    appointment_date: Optional[str] = None