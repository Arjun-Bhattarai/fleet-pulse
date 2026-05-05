#kun driver nagik xa passenger ko location sanga, tyo driver lai match garne logic ani tyo driver lai passenger ko location sanga match garne logic
from ..models.user import DriverLocation, Signal
from .driver_location_service import DriverLocationService
from ..utility.location import LocationUtility
from ..services.signal import SignalService
 
class MatchingService:
    def __init__(self, driver_location_service: DriverLocationService, signal_service: SignalService):
        self.driver_location_service = driver_location_service
        self.signal_service = signal_service 
 
    def match_drivers_to_signals(self, driver_locations: list[DriverLocation], signals: list[Signal], radius_km: float = 5.0):
        matched_results = []
        for driver_location in driver_locations:
            nearby_signals = []
            for signal in signals:
                distance = LocationUtility.calculate_distance(
                    driver_location.latitude, driver_location.longitude, signal.latitude, signal.longitude
                )
                if distance <= radius_km:
                    nearby_signals.append((signal, distance))
        nearby_signals.sort(key=lambda x: x[1])
        matched_results.append({
            "driver_id": driver_location.user_id,
            "nearby_signals": nearby_signals
        })
        return matched_results