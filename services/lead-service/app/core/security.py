import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

security = HTTPBearer()

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

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
    
async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    
    token = credentials.credentials
    user_data = await verify_token(token)

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Недействительный токен",
                            headers={"WWW-Authenticate": "Bearer"})

    if not user_data.get("is_active"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь неактивен")
    
    return user_data

async def get_current_manager(current_user: dict = Depends(get_current_user)) -> dict:
    role = current_user.get("role")
    if not role == "manager" and not role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав для выполнения этого действия")
    
    return current_user

async def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    
    if not current_user.get("role") == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав для выполнения этого действия")
    
    return current_user