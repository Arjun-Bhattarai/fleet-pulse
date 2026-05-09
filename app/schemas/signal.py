from pydantic import  BaseModel, Field,ConfigDict
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime, timezone

class SignalCreate(SQLModel):
    longitude: float
    latitude: float
    count: int = Field(..., ge=1)

class SignalUpdate(SQLModel):          
    longitude: Optional[float] = None
    latitude:  Optional[float] = None
    count: Optional[int] = Field(None, ge=1)

class SignalResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    longitude: float
    latitude: float
    count: int
    user_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SignalNearbyResponse(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    signals: SignalResponse
    distance_km: float


