from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(0, ge=0)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: int
    is_adult: bool
    created_at: datetime
    updated_at: datetime

