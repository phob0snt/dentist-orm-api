from fastapi import FastAPI
from app.api import leads

app = FastAPI(title="Dentist CRM Leads", version="1.0.0")

app.include_router(leads.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}