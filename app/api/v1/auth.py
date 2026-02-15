from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_active_user
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService
from app.schemas.auth import LoginRequest, Token, TokenLoginRequest
from app.core.security import verify_password, create_access_token


router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    #check existing user
    existing_user = UserService.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    #create non existing user

    try:
        user = UserService.create_user(db, user_in)
        db.commit()
        return {
            "message": "User created successfully",
            "username": user_in.name
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from e
    
@router.post("/login", response_model=Token)
def token(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, login_data.username) #confirm if it's username or name

    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code= 400, detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")    
    
    
    access_token = create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}




# @router.post("/token", response_model=Token)
# def token(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = UserService.get_user_by_email(db, login_data.username) #confirm if it's username or name
#     if not user or not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code= 400, detail="Invalid email or password"
#         )
#     access_token = create_access_token(email=user.email)
#     return {"access_token": access_token, "token_type": "bearer"}