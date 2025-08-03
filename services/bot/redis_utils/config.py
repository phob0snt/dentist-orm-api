from pydantic import BaseModel


class RedisTTLSettings(BaseModel):
    user_data: int = 3600
    leads_data: int = 300

redis_ttl_config = RedisTTLSettings()