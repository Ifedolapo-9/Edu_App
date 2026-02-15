from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead
from app.api.deps import get_db, get_current_active_user, get_current_active_admin
from app.models.enrollment import Enrollment
from app.services.enrollment import EnrollmentService
from app.models.user import User


router = APIRouter()


@router.post("/", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def student_enroll(
    enrollment_in: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    enrollment = EnrollmentService.enroll_student(
        db,
        enrollment_in.user_id,
        enrollment_in.course_id
    )

    if not enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled")

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/", response_model=list[EnrollmentRead])
def list_enrollments(
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    enrollments = (
        db.query(Enrollment)  
        .offset(skip)
        .limit(limit)
        .all()
    )

    return enrollments


@router.get("/course/{course_id}", response_model=list[EnrollmentRead], status_code=status.HTTP_200_OK)
def course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    enrollment = EnrollmentService.enrollments_for_course(
        db,
        course_id
    )

    if not enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled")

    return enrollment

@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def student_deregister(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),

):
    enrollment = EnrollmentService.deregister_student(
        db,
        current_user.id,
        course_id
    )

    if not enrollment:
        raise HTTPException(status_code=400, detail="Not Registered or already deregistered")

    return {"message": "Successfully deregistered"}