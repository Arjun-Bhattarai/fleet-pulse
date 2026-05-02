from pydantic import  Field,ConfigDict
from sqlmodel import SQLModel
from typing import Optional
import datetime

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
    created_at: datetime.datetime

