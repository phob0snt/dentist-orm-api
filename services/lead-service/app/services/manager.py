from fastapi import HTTPException, status
from app.core.security import get_password_hash
from app.crud import manager as manager_crud
from app.models.manager import ManagerORM
from app.schemas.manager import ManagerCreate, ManagerUpdate
from sqlalchemy.orm import Session


def create_manager(manager_data: ManagerCreate, db: Session) -> ManagerORM:
    existing_manager = db.query(ManagerORM).filter(
        ManagerORM.login == manager_data.login
        or ManagerORM.email == manager_data.email).first()

    if existing_manager is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Менеджер с таким логином или почтой уже существует"
        )

    return manager_crud.create_manager(manager_data, db)

def get_all_managers(db: Session) -> list[ManagerORM]:
    return manager_crud.get_all_managers(db)

def get_manager_by_id(manager_id: int, db: Session) -> ManagerORM:

    manager = manager_crud.get_manager_by_id(manager_id, db)

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Менеджер не найден"
        )
    
    return manager

def update_manager(manager_id: int, manager_data: ManagerUpdate, db: Session) -> ManagerORM:
    manager = get_manager_by_id(manager_id, db)
    
    update_data = manager_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    if "login" in update_data and update_data["login"] != manager.login:
        if manager_crud.get_by_login(update_data["login"], db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Менеджер с таким логином уже существует"
            )

    return manager_crud.update_manager(manager, db, update_data)

def delete_manager(manager_id: int, db: Session, current_admin: ManagerORM) -> None:
    manager = get_manager_by_id(manager_id, db)
    
    if manager.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя удалить себя"
        )
    
    manager_crud.delete_manager(manager, db)