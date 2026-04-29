# models/user.py
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    admin = "admin"
    driver = "driver"
    user = "user"

class User(SQLModel, table=True):
    __tablename__ = "users"  

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    hashed_password: str = Field(..., min_length=6, max_length=72)
    role: UserRole = Field(default=UserRole.driver)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
