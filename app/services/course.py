from app.models.course import Course
from sqlalchemy.orm import Session

from app.schemas.course import CourseCreate, CourseUpdate
from app.core.security import get_password_hash

class CourseService:

    @staticmethod
    def get_course(db_session: Session, course_id: int):
        return db_session.query(Course).filter(Course.id == course_id).first()
    
    @staticmethod
    def update_course(db_session: Session, course_id: int,  course_update: CourseUpdate):
        course = db_session.query(Course).filter(Course.id == course_id).first()
    
        if not course:
            return None
        
        update_data = course_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(course, key, value)
        
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        return course
    

    @staticmethod
    def course_status (db_session: Session, course_id: int, is_active: bool):
        course = db_session.query(Course).filter(Course.id == course_id).first()

        if not course:
            return None

        course.is_active = is_active

        
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        return course
    