from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.user import User
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.enrollment import EnrollmentCreate
from app.core.security import get_password_hash

class EnrollmentService:

    @staticmethod
    def enroll_student(db_session: Session, user_id: int, course_id: int):
        
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Inactivate user cannot enroll")

        course = db_session.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course ont found")

        if not course.is_active:
            raise HTTPException(status_code=403, detail="Cannot enroll in active course")


        existing = db_session.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first ()

        if existing: 
            raise HTTPException (status_code=400, detail="Already enrolled")
            
        current_enrollments = db_session.query(Enrollment).filter(
            Enrollment.course_id == course_id
        ).count()

        if current_enrollments >= course.capacity:
            raise HTTPException(status_code=400, detail="Course capacity reached")

        enrollment = Enrollment(user_id=user_id, course_id=course_id)

        db_session.add(enrollment)
        db_session.commit()
        db_session.refresh(enrollment)
        return enrollment

    
    @staticmethod
    def deregister_student(db_session: Session, user_id: int, course_id: int):
        
        enrollment = db_session.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first ()

        if not enrollment: 
            return None
        
        db_session.delete(enrollment)
        db_session.commit()

        return True

    @staticmethod
    def enrollments_for_course(db_session: Session, course_id:int):
        
        enrollments = db_session.query(Enrollment).filter(
            Enrollment.course_id == course_id
        ).all()

        if not enrollments:
            return None

        return enrollments

    # @staticmethod
    # def update_course(db_session: Session, course_id: int,  course_update: CourseUpdate):
    #     course = db_session.query(Course).filter(Course.id == course_id).first()
    
    #     if not course:
    #         return None
        
    #     update_data = course_update.model_dump(exclude_unset=True)
        
    #     for key, value in update_data.items():
    #         setattr(course, key, value)
        
    #     db_session.add(course)
    #     db_session.commit()
    #     db_session.refresh(course)

    #     return course
    

    # @staticmethod
    # def course_status (db_session: Session, course_id: int, is_active: bool):
    #     course = db_session.query(Course).filter(Course.id == course_id).first()

    #     if not course:
    #         return None

    #     course.is_active = is_active

        
    #     db_session.add(course)
    #     db_session.commit()
    #     db_session.refresh(course)

    #     return course
    