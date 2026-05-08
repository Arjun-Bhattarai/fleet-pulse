from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core.db import engine
from app.routes import auth, driver_location_route, signal_route, matching_route, role_change
import asyncio
from sqlalchemy.exc import OperationalError



@asynccontextmanager
async def lifespan(app: FastAPI):
    for i in range(10):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            print("✅ DB connected")
            break
        except OperationalError:
            print(f"DB not ready... retry {i+1}/10")
            await asyncio.sleep(2)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(driver_location_route.router, prefix="/driver-locations")
app.include_router(signal_route.router, prefix="/signals")
app.include_router(matching_route.route, prefix="/matching")
app.include_router(role_change.router, prefix="/role-change")