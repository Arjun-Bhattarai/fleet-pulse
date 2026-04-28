from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.db import get_session, get_db
from ..models.user import User
from sqlalchemy.future import select
from ..schemas.user import UserLogin, UserRegister, UserResponse
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register(info: UserRegister, db: AsyncSession = Depends(get_session)):

    result = await db.execute(select(User).where(User.email == info.email)) #yo email paila register vayeko xa ki xaina herxa 
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(info.password) #yo password lai hash garxa


    user = User(username=info.username, email=info.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"message": f"Registration Success for: {user.username}"}


@router.post("/login")
async def login(info: UserLogin, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.email == info.email))
    user=result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password or the user is not registered")
    
    password_check=pwd_context.verify(info.password, user.hashed_password)

    if not password_check:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": f"Login Success for: {user.username}"}


@router.get("/profile")
async def get_profile(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    users = result.scalar_one_or_none()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    else:
        return {"message": "Profile fetched successfully", "users": users}