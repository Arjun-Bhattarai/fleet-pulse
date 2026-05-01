from pydantic import SQLModel, Field
from sqlmodel import SQLModel, Field,Optional

class SignalCreate(SQLModel):
    longitude: float
    latitude: float
    count: int = Field(..., ge=0)

class SignalUpdate(SQLModel):          
    longitude: Optional[float] = None
    latitude:  Optional[float] = None
    country:   Optional[int]   = None