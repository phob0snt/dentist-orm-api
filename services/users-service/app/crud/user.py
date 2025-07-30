from app.schemas.user import UserCreate

from sqlalchemy.orm import Session
from app.models.user import UserORM

def create_user_data(data: UserCreate, auth_id: int, db: Session) -> UserORM | None:
    existing_user = db.query(UserORM).filter(UserORM.auth_id == auth_id).first()

    if existing_user is not None:
        return None
    
    user = UserORM(
        auth_id = auth_id,
        telegram_id = data.telegram_id,
        full_name = data.full_name,
        contact_phone = data.contact_phone
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_data(auth_id: int, db: Session) -> UserORM | None:
    return db.query(UserORM).filter(UserORM.auth_id == auth_id).first()

def get_user_data_by_tg(tg_id: str, db: Session) -> UserORM | None:
    return db.query(UserORM).filter(UserORM.telegram_id == tg_id).first()