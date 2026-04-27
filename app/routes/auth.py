from fastapi import APIRouter
from ..schemas.user import UserLogin, UserRegister, UserResponse

router = APIRouter()


@router.post("/register")
def register(info: UserRegister):
    return {"message": f"Registration Success for: {info.username}"}


@router.post("/login")
def login(info: UserLogin):
    return {"message": f"Login Success for: {info.username}"}


@router.get("/profile")
def get_profile():
    return {"message": "Profile fetched successfully"}