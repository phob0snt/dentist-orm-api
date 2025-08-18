import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import users
from app.services import users_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(users_consumer.run())
    yield
    await users_consumer.disconnect()


app = FastAPI(title="Dentist CRM Users", version="1.0.0", lifespan=lifespan)

app.include_router(users.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}