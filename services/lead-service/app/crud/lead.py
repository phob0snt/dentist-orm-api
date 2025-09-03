from app.schemas.lead import LeadCreate, LeadUpdate
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

def get_leads_by_user_id(user_id: int, db: Session) -> list[LeadORM] | None:
    return db.query(LeadORM).filter(LeadORM.user_id == user_id).all()

def update_lead(lead: LeadORM, lead_update: LeadUpdate, db: Session):
    data = lead_update.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(lead, field, value)

    db.commit()
    db.refresh(lead)
    return lead