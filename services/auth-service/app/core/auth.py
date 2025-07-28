from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import security
from app.core.security import verify_token
from app.db.session import get_db
from app.schemas.auth import AccountRole
from app.models.auth import AuthORM

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)) -> AuthORM:
    
    token = credentials.credentials
    login = verify_token(token)

    if login is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Недействительный токен",
                            headers={"WWW-Authenticate": "Bearer"})
    
    user = db.query(AuthORM).filter(AuthORM.login == login).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь не найден")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь неактивен")
    
    return user

def get_current_admin(current_user: AuthORM = Depends(get_current_user)
                      ) -> AuthORM:
    
    if current_user.role != AccountRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав для выполнения этого действия")
    
    return current_user