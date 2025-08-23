from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponce
from app.crud import user as user_crud

def create_user_data(user: UserCreate, auth_id: int, db: Session):
    data = user_crud.create_user_data(user, auth_id, db)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже существует"
        )
    
    created_data = UserResponce(
        telegram_id=data.telegram_id,
        full_name=data.full_name,
        contact_phone=data.contact_phone,
        id=data.id,
        auth_id=data.auth_id
    )
    
    return created_data

def get_user_data(token_payload: dict, db: Session):
    auth_id = token_payload.get("auth_id")
    if not auth_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Неверный токен"
        )
    
    user = user_crud.get_user_data(auth_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user

def get_user_data_by_tg(tg_id: str, db: Session):
    user = user_crud.get_user_data_by_tg(tg_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user

def get_tg_by_user_id(user_id: int, db: Session):
    tg_id = user_crud.get_tg_by_user_id(user_id, db)
    if not tg_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return tg_id