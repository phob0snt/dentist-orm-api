from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_admin, get_current_manager
from app.services import manager as manager_service
from app.models.manager import ManagerORM
from app.db.session import get_db
from app.schemas.manager import ManagerCreate, ManagerResponse, ManagerUpdate


router = APIRouter(prefix="/managers", tags=["managers"])

@router.post("/", response_model=ManagerResponse, status_code=status.HTTP_201_CREATED)
def create_manager(
    manager_data: ManagerCreate,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin)
):
    return manager_service.create_manager(manager_data, db)

@router.get("/", response_model=list[ManagerResponse])
def get_all_managers(
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin)
):
    return manager_service.get_all_managers(db)

@router.get("/me", response_model=ManagerResponse)
def get_current_manager(
    manager: ManagerORM = Depends(get_current_manager)
):
    return manager

@router.get("/{manager_id}", response_model=ManagerResponse)
def get_manager_by_id(
    manager_id: int,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin)
):
    return manager_service.get_manager_by_id(manager_id, db)

@router.put("/{manager_id}", response_model=ManagerResponse)
def update_manager(
    manager_id: int,
    manager_data: ManagerUpdate,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_admin),
):
    return manager_service.update_manager(manager_id, manager_data, db)

@router.delete("/{manager_id}")
def delete_manager(
    manager_id: int,
    db: Session = Depends(get_db),
    admin: ManagerORM = Depends(get_current_admin)
):
    manager_service.delete_manager(manager_id, db, admin)