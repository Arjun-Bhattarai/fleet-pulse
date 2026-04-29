from fastapi import FastAPI
from app.routes import auth
from sqlmodel import SQLModel
from app.core.db import engine

from app.models.user import User  

app = FastAPI()

app.include_router(auth.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)