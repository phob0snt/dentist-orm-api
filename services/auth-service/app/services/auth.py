from datetime import timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.auth import AuthORM
from app.schemas.auth import AccountCreate, AccountLogin, AccountResponce, AccountRole, RefreshRequest, TokenPair
import app.crud.account as account_crud
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)

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

    return AccountResponce(
        id=user.id,
        login=user.login,
        role=user.role,
        is_active=user.is_active,
        token_pair=create_token_pair(user)
    )

def refresh_token_pair(refresh_token: RefreshRequest, db: Session) -> TokenPair:
    user_data = verify_token(refresh_token.refresh_token, "refresh")

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh токен")
    
    user = account_crud.get_account_by_login(user_data.get("login"), db)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден или неактивен"
        )
    
    return create_token_pair(user)
    

def create_token_pair(user: AuthORM) -> TokenPair:
    access_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_expires = timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = create_access_token(
        data={
            "login": user.login,
            "auth_id": user.id,
            "role": user.role
        },
        expires_delta=access_expires
    )

    refresh_token = create_refresh_token(
        data={
            "login": user.login,
            "auth_id": user.id,
            "role": user.role
        },
        expires_delta=refresh_expires
    )

    return TokenPair(access_token=access_token, refresh_token=refresh_token)

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

def register_user_with_login(
        register_data: AccountCreate,
        role: AccountRole,
        db: Session) -> AccountResponce:
    
    user = register_user(register_data, role, db)

    return AccountResponce(
        id=user.id,
        login=user.login,
        role=user.role,
        is_active=user.is_active,
        token_pair=create_token_pair(user)
    )

def get_all_users(db: Session):
    return account_crud.get_all_accounts(db)

def disable_user(account_id: int, db: Session):
    user = account_crud.get_account_by_id(account_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким id не найден"
        )
    
    return account_crud.disable_account(user, db)

def enable_user(account_id: int, db: Session):
    user = account_crud.get_account_by_id(account_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким id не найден"
        )
    
    return account_crud.enable_account(user, db)