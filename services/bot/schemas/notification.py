from pydantic import BaseModel


class BotMessage(BaseModel):
    chat_id: int
    message: str