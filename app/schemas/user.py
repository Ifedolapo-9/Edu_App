from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal

class UserBase(BaseModel):
    email: EmailStr
    name: Optional [str] = None    
    role: Literal ["student", "admin"]

    

class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    
    # is_superuser: bool

    model_config = ConfigDict(from_attributes=True)