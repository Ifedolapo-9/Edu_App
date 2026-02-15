from sqlalchemy import Boolean, DateTime, Column, Integer, ForeignKey, Numeric, String, func, UniqueConstraint
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.db.base import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column (Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column (Integer, ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
   
    user = relationship("User")
    course = relationship("Course")

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="unique_enrollment"),
    )