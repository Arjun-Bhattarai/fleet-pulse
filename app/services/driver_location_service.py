from ..models.user import DriverLocation
from datetime import datetime, timezone
from sqlalchemy import select


class DriverLocationService:
    def __init__(self, session):
        self.session = session

    async def update_driver_location(self, user_id: int, longitude: float, latitude: float):
#        DriverLocation ko xa tyo update garna ko lagi, driver le aafno location update garna ko lagi
        result = await self.session.execute(
            select(DriverLocation).where(DriverLocation.user_id == user_id)
        )
        existing_location = result.scalar_one_or_none()
         #UPSERT logic: if existing_location xa bhane update garne, nabhane naya record create garne
        if existing_location:
            existing_location.longitude = longitude
            existing_location.latitude = latitude
            existing_location.updated_at = datetime.now(timezone.utc)

        else:
            existing_location = DriverLocation(
                user_id=user_id,
                longitude=longitude,
                latitude=latitude,
                updated_at=datetime.now(timezone.utc)
            )
            self.session.add(existing_location)

        await self.session.commit()
        await self.session.refresh(existing_location)

        return existing_location

    async def get_driver_location(self, user_id: int):

        result = await self.session.execute(
            select(DriverLocation).where(DriverLocation.user_id == user_id)
        )

        return result.scalar_one_or_none()