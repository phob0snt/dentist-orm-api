from datetime import timedelta
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.manager import ManagerORM
from app.schemas.manager import ManagerLogin, Token

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

@router.post("/login", response_model=Token)
def login(login_data: ManagerLogin, db: Session = Depends(get_db)):
    user = db.query(ManagerORM).filter(ManagerORM.login == login_data.login).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверный логин или пароль")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь неактивен")
    
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.login},
                                       expires_delta=access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer")