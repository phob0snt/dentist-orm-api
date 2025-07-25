from app.schemas.lead import LeadCreate
from sqlalchemy.orm import Session
from app.models.lead import LeadORM

def create_lead(lead_data: LeadCreate, db: Session) -> LeadORM:
    new_lead = LeadORM(**lead_data.model_dump())

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead

def get_all_leads(db: Session) -> list[LeadORM]:
    return db.query(LeadORM).all()

def get_lead_by_id(lead_id: int, db: Session) -> LeadORM | None:
    return db.query(LeadORM).filter(LeadORM.id == lead_id).first()

def update_lead_status(lead: LeadORM, new_status: str, db: Session):
    lead.status = new_status

    db.commit()
    db.refresh(lead)

    return lead