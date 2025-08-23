import asyncio
from contextlib import asynccontextmanager
import logging
import sys
from fastapi import FastAPI

from app.api import leads
from app.services.lead_rpc import lead_consumer
@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(lead_consumer.run())
    
    try:
        yield
    finally:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
        
        await lead_consumer.disconnect()

app = FastAPI(title="Dentist CRM Leads", version="1.0.0", lifespan=lifespan)

app.include_router(leads.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}