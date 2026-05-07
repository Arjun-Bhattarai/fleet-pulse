from ..models.user import DriverLocation, User
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.db import get_session
from ..core.security import get_current_user
from ..services.driver_location_service import DriverLocationService

router = APIRouter(tags=["driver-location"])

# Driver ko location update garna ko lagi service method

@router.put("/driver/location", response_model=DriverLocation)  # driver le aafno location update garna ko lagi
async def update_driver_location(longitude: float, latitude: float, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    driver_location_service = DriverLocationService(session)
    updated_location = await driver_location_service.update_driver_location(current_user.id, longitude, latitude)
    return updated_location