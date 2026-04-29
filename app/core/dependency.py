from fastapi import Request,HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.security import decode_access_token, get_current_user
from app.core.redis import token_in_blocklist
class AccessToken(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        token_data = decode_access_token(credentials.credentials)

        if await token_in_blocklist(token_data.get("jti")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is blacklisted",
            )

        self.verify_token_data(token_data)
        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError
class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission",
            )
        return True
