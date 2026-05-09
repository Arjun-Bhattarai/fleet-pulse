from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.db import get_session
from ..models.user import DriverLocation
from ..services.matching_service import MatchingService
from ..services.driver_location_service import DriverLocationService
from ..services.signal import SignalService
from ..schemas.matching_schema import NearbySignalResponse, DriverMatchResponse

route = APIRouter(tags=["matching"])


@route.get("/matching/drivers-signals", response_model=list[DriverMatchResponse])
async def match_drivers_to_signals(
    session: AsyncSession = Depends(get_session)
):

    driver_location_service = DriverLocationService(session)
    signal_service = SignalService(session)
    matching_service = MatchingService(driver_location_service, signal_service)

    result = await session.execute(select(DriverLocation))
    driver_locations = result.scalars().all()

    matched_results = await matching_service.match_drivers_to_signals(driver_locations)

    response = []

    for match in matched_results:

        nearby_signals_response = []

        for signal_data in match["nearby_signals"]:

            nearby_signals_response.append(
                NearbySignalResponse(
                    signal_id=signal_data["signal_id"],
                    latitude=signal_data["latitude"],
                    longitude=signal_data["longitude"],
                    count=signal_data["count"],
                    distance_km=signal_data["distance_km"]
                )
            )

        response.append(
            DriverMatchResponse(
                driver_id=match["driver_id"],
                nearby_signals=nearby_signals_response
            )
        )

    return response