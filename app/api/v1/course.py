from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.api.deps import get_db, get_current_active_user, get_current_active_admin
from app.models.course import Course
from app.services.course import CourseService


router = APIRouter()

@router.post("/create_course", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
): 
    course = Course(**course_in.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/all", response_model=list[CourseRead])
def list_courses(
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db),
):
    courses = (
        db.query(Course)
        .filter(Course.is_active==True)  #check syntax
        .offset(skip)
        .limit(limit)
        .all()
    )

    return courses

@router.get("/{course_id}", response_model=CourseRead)
def get_course_by_id(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = CourseService.get_course(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id{course_id} not found"
            )
    return course

@router.put("/{course_id}", response_model=CourseRead)
#diff function name than what is defined in services
def update_course_by_id(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    course = CourseService.update_course(db, course_id, course_update)


    if not course:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id {course_id} not found"
            )
    return course

@router.patch("/{course_id}/activate/{is_activate}", response_model=CourseRead)
#diff function name than what is defined in services
def activate_or_deactivate_course(
    course_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    course = CourseService.course_status(db, course_id, is_active)


    if not course:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id {course_id} not found"
            )
    return course

