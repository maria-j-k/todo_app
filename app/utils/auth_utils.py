import secrets
from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.models.consts import TOKEN_MAP, TokenTypes
from app.schemas import AuthToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def create_token(
    token_type: TokenTypes,
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> AuthToken:
    token_settings = TOKEN_MAP[token_type]
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            token_settings["expires"],  # type: ignore[arg-type]
        )
    payload = {
        "exp": expire,
        "sub": str(subject),
    }
    access_token = jwt.encode(
        payload, token_settings["secret"], algorithm=settings.algorithm
    )
    return AuthToken(token=access_token)


def generate_temporary_password():
    return secrets.token_urlsafe(15)
