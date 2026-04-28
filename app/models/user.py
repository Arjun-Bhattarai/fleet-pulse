# models/user.py
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    admin = "admin"
    driver = "driver"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.driver)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
