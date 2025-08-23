import asyncio
import logging
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import users
from app.services import users_rpc

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(users_rpc.run())
    
    try:
        yield
    finally:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
        
        await users_rpc.disconnect()


app = FastAPI(title="Dentist CRM Users", version="1.0.0", lifespan=lifespan)

app.include_router(users.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}