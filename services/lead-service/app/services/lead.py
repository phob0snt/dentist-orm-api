from fastapi import HTTPException, status
from app.schemas.lead import LeadCreate, LeadUpdate
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

def get_leads_by_user_id(user_id: int, db: Session) -> LeadORM:
    leads = lead_crud.get_leads_by_user_id(user_id, db)

    if not leads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leads not found"
        )
    
    return leads

def update_lead(
        lead_id: int,
        lead_update: LeadUpdate,
        db: Session
) -> LeadORM:
    lead = lead_crud.get_lead_by_id(lead_id, db)

    return lead_crud.update_lead(lead, lead_update, db)