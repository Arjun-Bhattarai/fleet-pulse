from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, DateTime
from typing import Optional
from datetime import datetime, timezone


class Signal(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(sa_column=Column(ForeignKey("users.id")))

    longitude: float
    latitude: float

    count: int = Field(default=0)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )

    def __repr__(self):
        return (
            f"Signal(user_id={self.user_id}, "
            f"lat={self.latitude}, lng={self.longitude}, count={self.count})"
        )