from datetime import timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import AccountCreate, AccountLogin, AccountRole, Token
import app.crud.account as account_crud
from app.core.security import verify_password, create_access_token

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


def authenticate_user(login_data: AccountLogin, db: Session):
    user = account_crud.get_account_by_login(login_data.login, db)

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль")
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь неактивен"
        )
    
    token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    token = create_access_token(data={"sub": user.login}, expires_delta=token_expires)
    
    return Token(access_token=token)

def register_user(
        register_data: AccountCreate,
        role: AccountRole,
        db: Session):
    user = account_crud.get_account_by_login(register_data.login, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует")

    return account_crud.create_account(register_data, role, db)

def delete_user(account_id: int, db: Session):
    user = account_crud.get_account_by_id(account_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким id не найден"
        )
    
    return account_crud.delete_account(user, db)