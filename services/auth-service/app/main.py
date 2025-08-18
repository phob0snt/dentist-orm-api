import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import auth
from app.services import auth_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(auth_consumer.run())
    
    try:
        yield
    finally:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
        
        await auth_consumer.disconnect()

app = FastAPI(title="Dentist CRM Auth", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Dentist CRM Auth Service"}