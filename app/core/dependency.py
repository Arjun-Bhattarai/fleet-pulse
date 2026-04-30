from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List

from app.core.security import decode_token, get_current_user
from app.core.redis import token_in_blocklist
from ..models.user import User


class AccessToken(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        credentials = await super().__call__(request)

        token_data = decode_token(credentials.credentials)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        if await token_in_blocklist(token_data.get("jti")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is blacklisted",
            )

        return token_data


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value == "admin":
            return current_user
        
        if current_user.role.value not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission",
            )

        return current_user