from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("token", token)
    data = decode_access_token(token)
    print("data", data)
    if data is None: 
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    user = db.query(User).filter(User.email == data.get("sub")).first()
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code = 400, detail="Inactive user")
    
    if current_user.role != UserRole.USER.value:
        raise HTTPException(status_code=403, detail="Student role required")
    
    return current_user

def get_current_active_admin(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive User")
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Admin user required")
    return current_user