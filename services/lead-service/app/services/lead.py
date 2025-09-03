import logging
import sys
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.lead import LeadCreate, LeadUpdate
from app.models.lead import LeadORM
from app.crud import lead as lead_crud
from .notification_producer import producer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


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

def get_leads_by_user_id(user_id: int, db: Session) -> list[LeadORM]:
    try:
        leads = lead_crud.get_leads_by_user_id(user_id, db)
        return leads
    except Exception as e:
        logger.error(f"Ошибка получения заявок пользователя: {e}")
        return []
        
async def update_lead(
        lead_id: int,
        lead_update: LeadUpdate,
        db: Session
) -> LeadORM:
    lead = lead_crud.get_lead_by_id(lead_id, db)
    lead_status = lead.status

    result = lead_crud.update_lead(lead, lead_update, db)
    logger.info(f"Updating lead {lead_status} {lead_update.status}")
    if lead_status != lead_update.status.value:
        body = {
            "lead_id": lead.id,
            "user_id": lead.user_id,
            "status": lead_update.status
        }
        if lead_update.appointment_date:
            body["appointment_date"] = lead_update.appointment_date.isoformat()
            
        await producer.publish(body)

    return result