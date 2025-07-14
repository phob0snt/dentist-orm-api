from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from sqlalchemy.orm import Session
from app.core.auth import get_current_admin, get_current_manager
from app.core.security import get_password_hash
from app.db.session import get_db
from app.models.manager import ManagerORM
from app.schemas.manager import ManagerCreate, ManagerResponse, ManagerUpdate


router = APIRouter(prefix="/managers", tags=["managers"])

@router.post("/", response_model=ManagerResponse, status_code=status.HTTP_201_CREATED)
def create_manager(
    manager_data: ManagerCreate,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin)
    ):
    
    existing_manager = db.query(ManagerORM).filter(
        ManagerORM.login == manager_data.login
        or ManagerORM.email == manager_data.email).first()

    if existing_manager is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Менеджер с таким логином или почтой уже существует"
        )
    
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

@router.get("/me", response_model=ManagerResponse)
def get_current_manager(
    current_user: ManagerORM = Depends(get_current_manager),
    ):

    return current_user

@router.get("/", response_model=list[ManagerResponse])
def get_all_managers(
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin)
    ):
    
    return db.query(ManagerORM).all()

@router.get("/{manager_id}", response_model=ManagerResponse)
def get_manager_by_id(
    manager_id: int,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin)
    ):

    manager = db.query(ManagerORM).filter(ManagerORM.id == manager_id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Менеджер не найден"
        )
    
    return manager

@router.put("/{manager_id}", response_model=ManagerResponse)
def update_manager(
    manager_id: int,
    manager_data: ManagerUpdate,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin)
    ):

    manager = db.query(ManagerORM).filter(ManagerORM.id == manager_id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Менеджер не найден"
        )
    
    update_data = manager_data.model_dump(exclude_unset=True)

    if ("password" in update_data):
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    if "login" in update_data and update_data["login"] != manager.login:
        existing_manager = db.query(ManagerORM).filter(
            ManagerORM.login == update_data["login"]).first()
        
        if existing_manager:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Менеджер с таким логином уже существует"
            )

    for field, value in update_data.items():
        setattr(manager, field, value)

    db.commit()
    db.refresh(manager)

    return manager

@router.delete("/{manager_id}")
def delete_manager(
    manager_id: int,
    db: Session = Depends(get_db),
    current_admin: ManagerORM = Depends(get_current_admin)
    ):

    manager = db.query(ManagerORM).filter(ManagerORM.id == manager_id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Менеджер не найден"
        )
    
    if manager.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя удалить себя"
        )
    
    db.delete(manager)
    db.commit()

    return {"detail": "Менеджер успешно удален"}