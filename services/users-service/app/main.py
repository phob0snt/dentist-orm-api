from fastapi import FastAPI
from app.api import users

app = FastAPI(title="Dentist CRM Users", version="1.0.0")

app.include_router(users.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}