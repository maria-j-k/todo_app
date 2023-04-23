from typing import cast

from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.config import settings
from app.models import User
from app.models.enums import TokenTypes
from app.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


TOKEN_TYPES_MAP = {
    TokenTypes.ACCESS: settings.secret_key_access,
    TokenTypes.REFRESH: settings.secret_key_refresh,
}


async def _get_current_user(
    token_type: TokenTypes, token: str = Depends(reusable_oauth2)
) -> User:
    secret = TOKEN_TYPES_MAP[token_type]
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.algorithm])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await User.get(cast(PydanticObjectId, token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_user(token: str = Depends(reusable_oauth2)) -> User:
    return await _get_current_user(token_type=TokenTypes.ACCESS, token=token)


async def get_current_user_form_refresh_token(
    token: str = Depends(reusable_oauth2),
) -> User:
    return await _get_current_user(token_type=TokenTypes.REFRESH, token=token)
