from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class LeadStatus(str, Enum):
    NEW = "new"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class LeadBase(BaseModel):
    service_type: str
    preferred_date: datetime
    appointment_date: Optional[datetime]
    comment: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    appointment_date: Optional[datetime] = None

class Lead(LeadBase):
    id: int
    status: LeadStatus
    created_at: datetime

    class Config:
        from_attributes = True
