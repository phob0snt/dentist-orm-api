from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base

class LeadORM(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    contact_phone = Column(String)
    contact_email = Column(String, nullable=True)
    service_type = Column(String)
    preferred_date = Column(DateTime)
    comment = Column(String, nullable=True)
    status = Column(String, default='new')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)