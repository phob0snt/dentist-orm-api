from fastapi import FastAPI
from app.api import leads
from app.api import managers
from app.api import auth

app = FastAPI(title="Dentist CRM API", version="1.0.0")

app.include_router(leads.router, prefix="/api")
app.include_router(managers.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}