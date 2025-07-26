from datetime import datetime
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Boolean

from app.models.base import Base

class AuthORM(Base):
    __tablename__ = 'auth_data'
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'manager', 'admin')",
            name='valid_user_role'
        ),
    )