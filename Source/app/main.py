from fastapi import FastAPI

from app.routers import managers

app = FastAPI(title="Dentist CRM API", version="1.0.0")

app.include_router(managers.router)

@app.get("/")
def read_root():
    return {"message": "Dentist CRM API"}