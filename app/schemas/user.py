from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class UserResponse(BaseModel):
    id: int
    firstname: Optional[str]
    lastname: Optional[str]
    username: str
    email: str
    role: str