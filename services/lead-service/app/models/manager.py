from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean

from app.models.base import Base

class ManagerORM(Base):
    __tablename__ = 'managers'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)