from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..core.db import get_session
from ..models.user import User, UserRole
from ..schemas.user import UserLogin, UserRegister, UserResponse
from ..core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    get_current_user,
)
from ..core.dependency import AccessToken, RoleChecker  
from app.services.service import AuthService

router = APIRouter()
user_service = AuthService()




@router.post("/register", response_model=UserResponse)
async def signup(
    user: UserRegister,
    session: AsyncSession = Depends(get_session)
):

    if await user_service.user_exists(user.email, user.username, session):
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    return await user_service.create_user(user, session)



@router.post("/login")
async def login(
    info: UserLogin,
    db: AsyncSession = Depends(get_session),
):
    user = await user_service.get_user_by_email(info.email, db)

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
        data={
            "uid": str(user.id),
            "email": user.email,
            "role": user.role.value,
        }
    )

    refresh_token = create_refresh_token(
        data={"uid": str(user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

#last ma modify garxu !!!!

@router.get("/admin-dashboard")
async def admin_dashboard(
    user: User = Depends(RoleChecker(["admin"]))
):
    return {"message": "This is the admin dashboard", "user": user.username}
@router.get("/driver-dashboard")
async def driver_dashboard(
    user: User = Depends(RoleChecker(["driver"]))
):
    return {"message": "This is the driver dashboard", "user": user.username}

@router.get("/user-dashboard")
async def user_dashboard(
    user: User = Depends(RoleChecker(["user"]))
):
    return {"message": "This is the user dashboard", "user": user.username}