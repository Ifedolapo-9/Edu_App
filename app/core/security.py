from typing import Optional 
from passlib.context import CryptContext 
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token (email: str, expires_delta: Optional [timedelta] = None) -> str: 
    if expires_delta is None:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    else:
        expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": email, "exp": expire}
    token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def decode_access_token(token: str) -> dict:
    try: 
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        print("payload", payload)
        return payload
    except InvalidTokenError:
        return None
