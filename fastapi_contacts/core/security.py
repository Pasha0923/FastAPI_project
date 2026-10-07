from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from core.config import settings


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str,hashed_password: str) -> bool:
    return password_hash.verify(password,hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expire, "type": "access"})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict,expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,))

    payload.update({"exp": expire, "type": "refresh"})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    if payload.get("type") != "access":
        raise ValueError("Invalid access token")

    return payload


def decode_refresh_token(token: str) -> dict:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    if payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")

    return payload