from pydantic import BaseModel

class LeadNotification(BaseModel):
    lead_id: int
    user_id: int
    status: str

class BotMessage(BaseModel):
    chat_id: str
    message: str