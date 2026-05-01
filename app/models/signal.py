from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime




class Signal(SQLModel, table=True):#user ka xa taha pauna!
    __tablename__ = "signals"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id:  int=Field( foreign_key="users.id")
    longitude: float = Field
    latitude: float = Field
    count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Signal(user_id={self.user_id}, longitude={self.longitude}, latitude={self.latitude}, count={self.count}, created_at={self.created_at})"