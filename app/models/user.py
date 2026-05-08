from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func
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
    hashed_password: str

    role: UserRole = Field(default=UserRole.user)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )


class DriverLocation(SQLModel, table=True):
    __tablename__ = "driver_locations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)

    longitude: float
    latitude: float

    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )