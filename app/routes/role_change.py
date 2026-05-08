from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_session
from ..models.user import User, UserRole
from ..core.security import get_current_user

router = APIRouter(tags=["role-change"])


@router.put("/make-driver/{user_id}")
async def make_driver(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)  # optional security
):

    # Admin la user lai driver banauna ko lagi matra allowed huncha
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not allowed")

    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = UserRole.driver

    await db.commit()
    await db.refresh(user)

    return {
        "message": "User promoted to driver",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }