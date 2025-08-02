import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: str = os.getenv("REDIS_PORT")

    bot_token: str = os.getenv("BOT_TOKEN")

    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")

    auth_service_url: str = os.getenv("AUTH_SERVICE_URL")
    users_service_url: str = os.getenv("USERS_SERVICE_URL")
    leads_service_url: str = os.getenv("LEADS_SERVICE_URL")

settings = Settings()