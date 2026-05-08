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
        result = await session.exec(select(User).where(User.id == user_id))
        return result.first()

    async def user_exists(self, email: str, username: str, session: AsyncSession):
        user_by_email = await self.get_user_by_email(email, session)
        user_by_username = await self.get_user_by_username(username, session)

        return user_by_email is not None or user_by_username is not None

    async def create_user(self, user_data: UserRegister, session: AsyncSession):
        data = user_data.model_dump()

        data["hashed_password"] = hash_password(data.pop("password"))

        # create user
        new_user = User(**data)
        new_user.role = UserRole.user

        session.add(new_user)

        try:
            await session.commit()
            await session.refresh(new_user)
        except Exception as e:
            await session.rollback()
            raise e

        return new_user