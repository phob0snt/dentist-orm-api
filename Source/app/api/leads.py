from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_manager
from app.models.manager import ManagerORM
from app.services import lead as lead_service

from app.db.session import get_db
from app.schemas.lead import Lead, LeadStatusUpdate


router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED)
def create_lead(lead_data = Lead, db: Session = Depends(get_db)):
    return lead_service.create_lead(lead_data, db)

@router.get("/", response_model=list[Lead])
def get_all_leads(
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_manager)
):
    return lead_service.get_all_leads(db)

@router.get("/{lead_id}", response_model=Lead)
def get_lead_by_id(
    lead_id: int,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_manager)
):
    return lead_service.get_lead_by_id(lead_id, db)

@router.patch("/{lead_id}", response_model=Lead)
def update_lead_status(
    lead_id: int,
    status_update: LeadStatusUpdate,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_manager)
):
    return lead_service.update_lead_status(lead_id, status_update, db)