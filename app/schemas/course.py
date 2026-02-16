from pydantic import BaseModel, ConfigDict #confirm field
from decimal import Decimal
from typing import Annotated, Optional


class CourseBase(BaseModel):
    title: str | None = None
    code: int 
    capacity: int
    is_active: bool = True

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)



class CourseUpdate(CourseBase):
    title: Optional [str] = None
    code: Optional [int] = None
    capacity: Optional [int] =  None
 
class CourseStatusUpdate(BaseModel):
    is_active: bool