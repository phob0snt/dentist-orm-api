from app.core.security import get_password_hash
from app.models.manager import ManagerORM
from app.schemas.manager import ManagerCreate
from sqlalchemy.orm import Session


def create_manager(manager_data: ManagerCreate, db: Session,) -> ManagerORM | None:
    
    existing_manager = db.query(ManagerORM).filter(
        ManagerORM.login == manager_data.login
        or ManagerORM.email == manager_data.email).first()

    if existing_manager is not None:
        return None
    
    new_manager = ManagerORM(
        full_name=manager_data.full_name,
        login=manager_data.login,
        email=manager_data.email,
        password_hash=get_password_hash(manager_data.password),
        is_active=manager_data.is_active,
        is_admin=manager_data.is_admin
    )

    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)

    return new_manager

def get_all_managers(db: Session) -> list[ManagerORM]:
    return db.query(ManagerORM).all()

def get_manager_by_id(manager_id: int, db: Session) -> ManagerORM | None:
    manager = db.query(ManagerORM).filter(ManagerORM.id == manager_id).first()

    if not manager:
        return None
    
    return manager

def get_by_login(login: str, db: Session) -> ManagerORM | None:
    return db.query(ManagerORM).filter(ManagerORM.login == login).first()

def update_manager(manager: ManagerORM, db: Session, data: dict) -> ManagerORM:
    for field, value in data.items():
        setattr(manager, field, value)

    db.commit()
    db.refresh(manager)

    return manager

def delete_manager(manager: ManagerORM, db: Session) -> None:
    db.delete(manager)
    db.commit()