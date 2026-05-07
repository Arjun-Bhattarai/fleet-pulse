# yo route le driver location haru lai nearby signals sanga match garne kaam garcha.
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.db import get_session
from ..services.matching_service import MatchingService
from ..services.driver_location_service import DriverLocationService
from ..services.signal import SignalService 
from ..schemas.matching_schema import NearbySignalResponse, DriverMatchResponse
from sqlalchemy import select
from ..models.user import DriverLocation


route = APIRouter(tags=["matching"])


@route.get("/matching/drivers-signals", response_model=list[DriverMatchResponse])
async def match_drivers_to_signals(session: AsyncSession = Depends(get_session)):
    driver_location_service = DriverLocationService(session)
    signal_service = SignalService(session)
    matching_service = MatchingService(driver_location_service, signal_service)

    # Sabai driver location haru fetch garne
    result = await session.execute(select(DriverLocation))
    driver_locations = result.scalars().all()

    # Driver haru lai nearby signals sanga match garne
    matched_results = await matching_service.match_drivers_to_signals(driver_locations)

    # Response format ma convert garne
    response = []
    for match in matched_results:
        nearby_signals_response = [
            NearbySignalResponse(
                signal_id=signal_data["signal"].id,
                latitude=signal_data["signal"].latitude,
                longitude=signal_data["signal"].longitude,
                count=signal_data["signal"].count,
                distance_km=signal_data["distance_km"]
            ) for signal_data in match["nearby_signals"]
        ]
        response.append(DriverMatchResponse(
            driver_id=match["driver_id"],
            nearby_signals=nearby_signals_response
        ))

    return response  