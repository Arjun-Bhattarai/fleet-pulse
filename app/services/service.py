from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from app.schemas.user import UserRegister
from ..models.user import User, UserRole
from app.core.security import hash_password


class AuthService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        result = await session.exec(select(User).where(User.email == email))
        return result.first()

    async def get_user_by_username(self, username: str, session: AsyncSession):
        result = await session.exec(select(User).where(User.username == username))
        return result.first()

    async def get_user_by_id(self, user_id: UUID, session: AsyncSession):
        result = await session.exec(select(User).where(User.uid == user_id))
        return result.first()

    async def user_exists(self, email: str, username: str, session: AsyncSession):
        return {
            "email": await self.get_user_by_email(email, session) is not None,
            "username": await self.get_user_by_username(username, session) is not None,
        }

    async def create_user(self, user_data: UserRegister, session: AsyncSession):
        data = user_data.model_dump()

        data["hashed_password"] = hash_password(data.pop("password"))

        new_user = User(**data)
        new_user.role = UserRole.user

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        except Exception:
            await session.rollback()
            raise

        return new_user