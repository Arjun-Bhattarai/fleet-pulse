from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import uuid
from app.config import config

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

security = HTTPBearer()



def hash_password(password: str) -> str:
    if not isinstance(password, str):
        raise HTTPException(400, "Password must be string")

    password = password.strip()

    if len(password) < 6:
        raise HTTPException(400, "Password too short")

    if len(password) > 72:
        raise HTTPException(400, "Password too long (max 72)")

    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)



def create_access_token(data: dict) -> str:
    payload = {
        "uid": str(data["uid"]),
        "role": data.get("role"),
        "exp": datetime.now(timezone.utc)
        + timedelta(seconds=config.ACCESS_TOKEN_EXPIRE),
        "jti": str(uuid.uuid4()),
        "type": "access",
    }

    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)



def create_refresh_token(data: dict) -> str:
    payload = {
        "uid": str(data["uid"]),
        "exp": datetime.now(timezone.utc)
        + timedelta(seconds=config.REFRESH_TOKEN_EXPIRE),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
    }

    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)



def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    return payload