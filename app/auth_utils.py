from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.schemas import AuthToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            settings.access_token_expires,
        )
    payload = {
        "exp": expire,
        "sub": str(subject),
    }
    access_token = jwt.encode(
        payload, settings.secret_key_access, algorithm=settings.algorithm
    )
    return AuthToken(token=access_token)


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            settings.refresh_token_expires,
        )
    payload = {
        "exp": expire,
        "sub": str(subject),
    }
    refresh_token = jwt.encode(
        payload, settings.secret_key_refresh, algorithm=settings.algorithm
    )
    return AuthToken(token=refresh_token)
