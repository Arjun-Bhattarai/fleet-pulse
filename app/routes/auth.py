from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..core.db import get_session
from ..models.user import User
from ..schemas.user import UserLogin, UserRegister, UserResponse
from ..core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    get_current_user,
)

router = APIRouter()



@router.post("/register")
async def register(
    info: UserRegister,
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(User).where(User.email == info.email)
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        username=info.username,
        email=info.email,
        hashed_password=hash_password(info.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"message": f"Registration Success for: {user.username}"}



@router.post("/login")
async def login(
    info: UserLogin,
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(User).where(User.email == info.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(info.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"uid": str(user.id), "role": user.role.value}
    )

    refresh_token = create_refresh_token(
        data={"uid": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }



@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user