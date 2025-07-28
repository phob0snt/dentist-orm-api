import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.auth import AuthORM
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY не найден в переменных окружения")

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль против хеша"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Создает хеш пароля"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создает JWT токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Проверяет JWT токен и возвращает логин пользователя"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            return None
        return login
    except JWTError:
        return None

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
) -> AuthORM:
    
    token = credentials.credentials
    user_login = verify_token(token)

    user_data = db.query(AuthORM).filter(AuthORM.login == user_login).first()

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Недействительный токен",
                            headers={"WWW-Authenticate": "Bearer"})

    if not user_data.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь неактивен")
    
    return user_data

async def get_current_manager(current_user: AuthORM = Depends(get_current_user)) -> AuthORM:
    role = current_user.role
    if role != "manager" and role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав для выполнения этого действия")
    
    return current_user

async def get_current_admin(current_user: AuthORM = Depends(get_current_user)) -> AuthORM:
    
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав для выполнения этого действия")
    
    return current_user