from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.auth import AuthORM
from app.schemas.auth import AccountCreate, AccountLogin, AccountResponce, AccountRole
from app.services import auth as auth_service
from app.core.auth import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(login_data: AccountLogin,
          db: Session = Depends(get_db)
):
    return auth_service.authenticate_user(login_data, db)

@router.post("/register", response_model=AccountResponce)
def register_user(register_data: AccountCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(register_data, AccountRole.USER, db)

@router.post("/admin/register_manager", response_model=AccountResponce)
def register_manager(
    register_data: AccountCreate,
    current_admin: AuthORM = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_admin.role != AccountRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недостаточно прав")
    
    return auth_service.register_user(register_data, AccountRole.MANAGER, db)

@router.get("/me", response_model=AccountResponce)
def get_current_user(user: AuthORM = Depends(get_current_user)):
    return user

@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    return auth_service.delete_user(account_id, db)