from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class LeadNotification(BaseModel):
    lead_id: int
    user_id: int
    status: Optional[str]
    appointment_date: Optional[str]

class BotMessage(BaseModel):
    chat_id: str
    message: str