from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    full_name: str
    role: Optional[str] = "taxpayer"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"

class UserResponse(UserBase):
    id: str
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

Token.model_rebuild()
