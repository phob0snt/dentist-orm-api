from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from .base import Base

class UserORM(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(Integer, index=True)
    telegram_id = Column(String)
    full_name = Column(String)
    contact_phone = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)