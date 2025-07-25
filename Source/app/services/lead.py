from fastapi import HTTPException, status
from app.schemas.lead import LeadCreate, LeadStatusUpdate
from app.models.lead import LeadORM
from app.crud import lead as lead_crud
from sqlalchemy.orm import Session


def create_lead(lead_data: LeadCreate, db: Session) -> LeadORM:
    return lead_crud.create_lead(lead_data, db)

def get_all_leads(db: Session) -> list[LeadORM]:
    return lead_crud.get_all_leads(db)

def get_lead_by_id(lead_id: int, db: Session) -> LeadORM:
    lead = lead_crud.get_lead_by_id(lead_id, db)

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    return lead

def update_lead_status(
        lead_id: int,
        status_update: LeadStatusUpdate,
        db: Session
) -> LeadORM:
    lead = lead_crud.get_lead_by_id(lead_id, db)

    return lead_crud.update_lead_status(lead, status_update.status, db)