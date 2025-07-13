from fastapi import FastAPI

from app.api import auth
from app.routers import managers

app = FastAPI(title="Dentist CRM API", version="1.0.0")

app.include_router(auth.router)
app.include_router(managers.router)

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}