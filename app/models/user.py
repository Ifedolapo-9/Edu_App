from sqlalchemy import Boolean, Column, Integer, String, func
from datetime import datetime, timezone
from enum import Enum
from app.db.base import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    name = Column (String, index=True)
    role = Column(String, default=UserRole.USER.value)