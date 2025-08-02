from typing import Optional
from pydantic import BaseModel

class LeadCreate(BaseModel):
    service_type: str
    preferred_date: str
    comment: Optional[str]