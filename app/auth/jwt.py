import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.auth.schemas import Token


# JWT configuration (must be provided via environment variables)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a short-lived JWT access token"""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a long-lived JWT refresh token"""
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Token:
    """Verify JWT token integrity and extract payload"""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False},
        )

        sub = payload.get("sub")
        if not sub:
            raise ValueError("Invalid token payload")

        return Token(sub=sub, exp=payload.get("exp"))

    except JWTError as e:
        raise ValueError("Invalid token") from e