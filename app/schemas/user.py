from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    driver = "driver"
    user= "user"

class UserRegister(BaseModel): #yesma role halnu hudina, default role user nai huncha
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: str
    email: EmailStr
    role: UserRole = UserRole.user

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
    role: UserRole