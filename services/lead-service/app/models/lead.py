from datetime import datetime
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Enum
import enum

from app.models.base import Base


class LeadStatus(enum.Enum):
    NEW = "new"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class LeadORM(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    contact_phone = Column(String)
    contact_email = Column(String, nullable=True)
    service_type = Column(String)
    preferred_date = Column(DateTime)
    appointment_date = Column(DateTime, nullable=True)
    comment = Column(String, nullable=True)
    status = Column(String, default=LeadStatus.NEW.value)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint(
            "status IN ('new', 'confirmed', 'cancelled')",
            name='valid_lead_status'
        ),
    )