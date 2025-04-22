from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserInfoResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None
    gender: Optional[str] = None
    provider: Optional[str] = None

    class Config:
        from_attributes = True  # SQLAlchemy 연동용

class VerifyPasswordRequest(BaseModel):
    password: str
class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

