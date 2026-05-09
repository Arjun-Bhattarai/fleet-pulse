from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_session
from ..core.security import hash_password
from ..core.dependency import RoleChecker
from ..models.user import User, UserRole
from ..schemas.user import UserRegister, UserResponse
from sqlmodel import select
router = APIRouter(tags=["admin"])



@router.post("/setup-admin", response_model=UserResponse)
async def setup_admin(
    data: UserRegister,
    db: AsyncSession = Depends(get_session)
):

    result = await db.execute(
        select(User).where(User.role == UserRole.admin)
    )

    existing_admin = result.scalar_one_or_none()

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )

    existing_email = await db.execute(
        select(User).where(User.email == data.email)
    )

    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_pw = hash_password(data.password)

    admin = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw,
        role=UserRole.admin
    )

    db.add(admin)

    await db.commit()
    await db.refresh(admin)

    return admin


@router.post("/create-driver", response_model=UserResponse)
async def create_driver(
    data: UserRegister,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(RoleChecker(["admin"]))
):

    existing_email = await db.execute(
        select(User).where(User.email == data.email)
    )

    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_pw = hash_password(data.password)

    driver = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw,
        role=UserRole.driver
    )

    db.add(driver)

    await db.commit()
    await db.refresh(driver)

    return driver


@router.post("/create-admin", response_model=UserResponse)
async def create_admin(
    data: UserRegister,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(RoleChecker(["admin"]))
):

    existing_email = await db.execute(
       select(User).where(User.email == data.email)
    )

    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_pw = hash_password(data.password)

    admin = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw,
        role=UserRole.admin
    )

    db.add(admin)

    await db.commit()
    await db.refresh(admin)

    return admin
