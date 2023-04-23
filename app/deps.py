from typing import Optional, cast

from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr, ValidationError

from app.config import settings
from app.models import User
from app.models.consts import TOKEN_MAP, TokenTypes
from app.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def _parse_token(
    token_type: TokenTypes, token: str = Depends(reusable_oauth2)
) -> Optional[str]:
    secret = TOKEN_MAP[token_type]["secret"]
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.algorithm])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data.sub


async def _get_current_user(
    token_type: TokenTypes, token: str = Depends(reusable_oauth2)
) -> User:
    sub = await _parse_token(token_type=token_type, token=token)
    user = await User.get(cast(PydanticObjectId, sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_user(token: str = Depends(reusable_oauth2)) -> User:
    return await _get_current_user(token_type=TokenTypes.ACCESS, token=token)


async def get_current_user_form_refresh_token(
    token: str = Depends(reusable_oauth2),
) -> User:
    return await _get_current_user(token_type=TokenTypes.REFRESH, token=token)


async def get_user_from_email_token(token: str = Depends(reusable_oauth2)) -> User:
    sub = await _parse_token(token_type=TokenTypes.EMAIL, token=token)
    email = cast(EmailStr, sub)
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
