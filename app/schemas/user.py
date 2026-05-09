from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    driver = "driver"
    user= "user"

class UserRegister(BaseModel): #yesma role halnu hudina, default role user nai huncha
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole


class DriverLocationCreate(BaseModel):
    longitude: float
    latitude: float