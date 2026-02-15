from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserRead
from app.api.deps import get_db, get_current_active_user
from app.models.user import User


router = APIRouter()

@router.get("/me", response_model=UserRead)
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return current_user
    
    