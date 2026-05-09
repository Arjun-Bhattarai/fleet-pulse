from pydantic import BaseModel

class NearbySignalResponse(BaseModel):
    signal_id: int
    latitude: float
    longitude: float
    count: int
    distance_km: float


class DriverMatchResponse(BaseModel):
    driver_id: int
    nearby_signals: list[NearbySignalResponse]
