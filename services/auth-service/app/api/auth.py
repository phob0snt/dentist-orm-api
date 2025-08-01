from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.auth import AuthORM
from app.schemas.auth import AccountCreate, AccountLogin, AccountResponce, AccountRole
from app.services import auth as auth_service
from app.core.security import get_current_admin, get_current_user


router = APIRouter(tags=["auth"])

@router.post("/login", response_model=AccountResponce)
def login(login_data: AccountLogin, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(login_data, db)

@router.post("/refresh")
def refresh_token(token: str, db: Session = Depends(get_db)):
    return auth_service.refresh_token_pair(token, db)

@router.post("/register", response_model=AccountResponce)
def register_user(register_data: AccountCreate, db: Session = Depends(get_db)):
    return auth_service.register_user_with_login(register_data, AccountRole.USER, db)

@router.get("/me", response_model=AccountResponce)
def get_current_user(user: AuthORM = Depends(get_current_user)):
    return user

@router.post("/admin/register_manager", response_model=AccountResponce)
def register_manager(
    register_data: AccountCreate,
    _: AuthORM = Depends(get_current_admin),
    db: Session = Depends(get_db)
):    
    return auth_service.register_user(register_data, AccountRole.MANAGER, db)

@router.get("/admin/users", response_model=list[AccountResponce])
def get_all_users(
    _: AuthORM = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return auth_service.get_all_users(db)

@router.post("/admin/disable/{account_id}")
def disable_account(
    account_id: int,
    _: AuthORM = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return auth_service.disable_user(account_id, db)

@router.post("/admin/enable/{account_id}")
def enable_account(
    account_id: int,
    _: AuthORM = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return auth_service.enable_user(account_id, db)