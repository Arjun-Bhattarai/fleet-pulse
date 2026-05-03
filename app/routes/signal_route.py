from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.db import get_session
from ..schemas.signal import SignalCreate, SignalResponse, SignalUpdate, SignalNearbyResponse
from ..services.signal import SignalService
from ..models.user import User
from ..core.dependency import RoleChecker
from ..core.security import get_current_user
from ..utility.location import LocationUtility

router = APIRouter()


@router.post("/signals",response_model=SignalResponse)  # user la send garako signal haru ko list
async def create_signal(signal: SignalCreate, session: AsyncSession = Depends(get_session),current_user: User = Depends(get_current_user)):
    signal_service = SignalService(session)
    created_signal = await signal_service.create_signal(signal, current_user.id)
    return created_signal


@router.get("/signals/my", response_model=list[SignalResponse])  # aafnu signal haru ko list
async def my_signals(session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    signal_service = SignalService(session)
    signals = await signal_service.get_signals(current_user.id)
    return signals


@router.get("/signals", response_model=list[SignalResponse],dependencies=[Depends(RoleChecker(["driver", "admin"]))])  # driver la sab ko signal herna ko lagi
async def get_all_signals(session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    signal_service = SignalService(session)
    signals = await signal_service.get_all_signals()
    return signals


@router.get("/signals/{signal_id}", response_model=SignalResponse,dependencies=[Depends(RoleChecker(["driver", "admin"]))])  # signal ko details
async def get_signal_by_id(signal_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    signal_service = SignalService(session)
    signal = await signal_service.get_signal_by_id(signal_id)
    return signal

@router.put("/signals/{signal_id}", response_model=SignalResponse)  # signal update garna ko lagi
async def update_signal_by_id(signal_id: int, signal_data: SignalUpdate, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    signal_service = SignalService(session)
    updated_signal = await signal_service.update_signal(signal_id, signal_data, current_user.id)
    return updated_signal


@router.delete("/signals/{signal_id}", response_model=SignalResponse)  # signal delete garna ko lagi
async def delete_signal_by_id(signal_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    signal_service = SignalService(session)
    deleted_signal = await signal_service.delete_signal(signal_id, current_user.id)
    return deleted_signal

# Nearby signals ko lagi endpoint, jasma user le latitude, longitude, ra radius_km pathaunecha, ani tyo radius bhitra parne signal haru ko list aauxa
@router.get("/signals/nearby", response_model=list[SignalNearbyResponse])  # nearby signal haru ko list
async def get_nearby_signals(latitude: float, longitude: float, radius_km: float=5.0, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    signal_service = SignalService(session)
    nearby_signals = await signal_service.get_prioritized_signals(latitude, longitude, radius_km)
    return nearby_signals
    