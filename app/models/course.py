from sqlalchemy import Boolean, Column, Integer, Numeric, String, func, CheckConstraint
from datetime import datetime, timezone

from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column (String, index=True)
    #try to make code three numbers limit wise
    code = Column(Integer, nullable=False)
    # try to make capacity greater than 0
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint("capacity > 0", name="capacity_positive"),
    )
   
