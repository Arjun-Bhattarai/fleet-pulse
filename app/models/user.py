# models/user.py
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime, timezone


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
    role: UserRole = Field(default=UserRole.user)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"User(username={self.username}, email={self.email}, role={self.role})"

class DriverLocation(SQLModel, table=True):# driver ko xa taha pauna! driver le location update garna
    __tablename__ = "driver_locations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True, foreign_key="users.id")
    longitude: float = Field(...)
    latitude: float = Field(...)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    def __repr__(self) -> str:
        return f"DriverLocation(user_id={self.user_id}, longitude={self.longitude}, latitude={self.latitude}, updated_at={self.updated_at})"