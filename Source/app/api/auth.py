from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.manager import ManagerLogin
from app.services.auth import authenticate_manager


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/")
def login(login_data: ManagerLogin,
          db: Session = Depends(get_db)
):
    return authenticate_manager(login_data, db)