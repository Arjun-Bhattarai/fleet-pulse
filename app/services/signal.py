from app.models.signal import Signal
from app.schemas.signal import SignalCreate, SignalUpdate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from ..utility.location import LocationUtility


class SignalService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_signal(self, signal_data: SignalCreate, user_id: int):
        new_signal = Signal(**signal_data.model_dump(), user_id=user_id)
        self.db_session.add(new_signal)
        await self.db_session.commit()
        await self.db_session.refresh(new_signal)
        return new_signal

    async def get_signals(self, user_id: int):
        result = await self.db_session.exec(
            select(Signal).where(Signal.user_id == user_id)
        )
        signals = result.all()
        if not signals:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No signals found for user {user_id}"
            )
        return signals

    async def get_all_signals(self):
        result = await self.db_session.exec(select(Signal))
        signals = result.all()
        if not signals:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No signals found"
            )
        return signals

    async def delete_signal(self, signal_id: int, user_id: int):  
        result = await self.db_session.exec(
            select(Signal).where(Signal.id == signal_id)

        )
        signal_to_delete = result.first()                       
        if not signal_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Signal {signal_id} not found"
            )
        if signal_to_delete.user_id != user_id:                 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this signal"
            )
        self.db_session.delete(signal_to_delete)
        await self.db_session.commit()
        return {"message": f"Signal {signal_id} deleted successfully"}

    async def update_signal(self, signal_id: int, signal_data: SignalUpdate, user_id: int):
        result = await self.db_session.exec(
            select(Signal).where(Signal.id == signal_id)
        )
        signal_to_update = result.first()
        if not signal_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Signal {signal_id} not found"
            )
        if signal_to_update.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this signal"
            )
        for field, value in signal_data.model_dump(exclude_unset=True).items():
            setattr(signal_to_update, field, value)
        self.db_session.add(signal_to_update)
        await self.db_session.commit()
        await self.db_session.refresh(signal_to_update)
        return signal_to_update
    
    async def get_signal_by_id(self, signal_id: int):
        result = await self.db_session.exec(
            select(Signal).where(Signal.id == signal_id)
        )
        signal = result.first()
        if not signal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Signal {signal_id} not found"
            )
        return signal
    
# user la driver ko location anusar signal haru prioritize garna ko lagi using sorting and distance calculation
    async def get_prioritized_signals(self, driver_lat: float, driver_long: float, radius_km: float = 5.0):
        result = await self.db_session.exec(select(Signal))
        signals = result.all()
        if not signals:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No signals found"
            )
        prioritized_signals = []
        for signal in signals:
            distance = LocationUtility.calculate_distance(driver_lat, driver_long, signal.latitude, signal.longitude)
            if distance <= radius_km:
                prioritized_signals.append((signal, distance))
        prioritized_signals.sort(key=lambda x: x[1])
        return [signal for signal, _ in prioritized_signals]
