from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    role: str