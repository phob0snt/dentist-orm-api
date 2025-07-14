from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_manager
from app.models.manager import ManagerORM
from app.schemas.lead import Lead, LeadCreate, LeadStatusUpdate
from app.models.lead import LeadORM
from app.db.session import get_db

router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED)
def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db),
    ):

    new_lead = LeadORM(
        full_name = lead_data.full_name,
        contact_phone = lead_data.contact_phone,
        contact_email = lead_data.contact_email,
        service_type = lead_data.service_type,
        preferred_date = lead_data.preferred_date,
        comment = lead_data.comment
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead


@router.get("/", response_model=list[Lead])
def get_all_leads(
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_manager)
    ):

    leads = db.query(LeadORM).all()
    return leads


@router.get("/{lead_id}", response_model=Lead)
def get_lead_by_id(
    lead_id: int,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_manager)
    ):

    lead = db.query(LeadORM).filter(LeadORM.id == lead_id).first()

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    return lead


@router.patch("/{lead_id}", response_model=Lead)
def update_lead_status(
    lead_id: int,
    status_update: LeadStatusUpdate,
    db: Session = Depends(get_db),
    _: ManagerORM = Depends(get_current_manager)
    ):

    lead = db.query(LeadORM).filter(LeadORM.id == lead_id).first()

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    lead.status = status_update.status
    db.commit()
    db.refresh(lead)

    return lead