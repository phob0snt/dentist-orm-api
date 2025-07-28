from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_manager
from app.services import lead as lead_service

from app.db.session import get_db
from app.schemas.lead import Lead, LeadCreate, LeadUpdate


router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED)
async def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    return lead_service.create_lead(lead_data, db)

@router.get("/", response_model=list[Lead])
async def get_all_leads(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_manager)
):
    return lead_service.get_all_leads(db)

@router.get("/{lead_id}", response_model=Lead)
async def get_lead_by_id(
    lead_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_manager)
):
    return lead_service.get_lead_by_id(lead_id, db)

@router.patch("/{lead_id}", response_model=Lead)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_manager)
):
    return lead_service.update_lead(lead_id, lead_update, db)