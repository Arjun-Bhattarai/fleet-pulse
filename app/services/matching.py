from ..models.user import DriverLocation
from .driver_location_service import DriverLocationService
from ..services.signal import SignalService

class MatchingService:
    def __init__(self, driver_location_service: DriverLocationService, signal_service: SignalService):
        self.driver_location_service = driver_location_service
        self.signal_service = signal_service 

    async def match_drivers_to_signals(self, driver_locations: list[DriverLocation], radius_km: float = 5.0):
        matched_results = []
        
        for driver_location in driver_locations:
            nearby_signals = await self.signal_service.get_prioritized_signals(
                driver_lat=driver_location.latitude, 
                driver_long=driver_location.longitude, 
                radius_km=radius_km
            )
            
            matched_results.append({
                "driver_id": driver_location.user_id,
                "nearby_signals": nearby_signals
            })
            
        return matched_results