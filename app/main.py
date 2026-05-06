from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core.db import engine
from app.routes import auth
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

app.include_router(auth.router)