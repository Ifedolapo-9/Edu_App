from pydantic import BaseModel, ConfigDict #confirm field
from decimal import Decimal
from datetime import datetime
from typing import Annotated, Optional


class EnrollmenteBase(BaseModel):
    user_id: int
    course_id: int 
    


class EnrollmentCreate(EnrollmenteBase):
    pass

class EnrollmentRead(EnrollmenteBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


 