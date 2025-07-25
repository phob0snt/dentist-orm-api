from datetime import timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.manager import ManagerLogin, Token
import app.crud.manager as manager_crud
from app.core.security import verify_password, create_access_token

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


def authenticate_manager(login_data: ManagerLogin, db: Session):
    manager = manager_crud.get_by_login(login_data.login, db)

    if not manager or not verify_password(login_data.password, manager.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль")
    
    if not manager.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь неактивен"
        )
    
    token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    token = create_access_token(data={"sub": manager.login}, expires_delta=token_expires)
    
    return Token(access_token=token)