from app.core.security import get_password_hash
from app.models.auth import AuthORM
from app.schemas.auth import AccountCreate, AccountRole
from sqlalchemy.orm import Session


def create_account(
        user_data: AccountCreate,
        role: AccountRole,
        db: Session
) -> AuthORM | None:
    new_user = AuthORM(
        login=user_data.login,
        password_hash=get_password_hash(user_data.password),
        role=role.value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_all_accounts(db: Session) -> list[AuthORM]:
    return db.query(AuthORM).all()

def get_account_by_id(manager_id: int, db: Session) -> AuthORM | None:
    manager = db.query(AuthORM).filter(AuthORM.id == manager_id).first()

    if not manager:
        return None
    
    return manager

def get_account_by_login(login: str, db: Session) -> AuthORM | None:
    return db.query(AuthORM).filter(AuthORM.login == login).first()

def update_account(manager: AuthORM, db: Session, data: dict) -> AuthORM:
    for field, value in data.items():
        setattr(manager, field, value)

    db.commit()
    db.refresh(manager)

    return manager

def delete_account(manager: AuthORM, db: Session) -> None:
    db.delete(manager)
    db.commit()