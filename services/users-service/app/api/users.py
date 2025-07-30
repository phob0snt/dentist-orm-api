from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponce
from app.core.security import get_current_admin, get_current_user
from app.db.session import get_db
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post('/profile', response_model=UserResponce)
def create_user_data(
    user: UserCreate,
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    auth_id = payload.get("auth_id")
    return user_service.create_user_data(user, auth_id, db)

@router.get('/profile', response_model=UserResponce)
def get_user_data(
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return user_service.get_user_data(payload, db)

@router.get('/by-telegram{tg_id}', response_model=UserResponce)
def get_user_data(
    tg_id: str,
    _: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return user_service.get_user_data_by_tg(tg_id, db)