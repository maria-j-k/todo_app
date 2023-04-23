from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.auth_utils import create_token, get_hashed_password
from app.crud import user as crud_user
from app.deps import get_current_user_form_refresh_token, get_user_from_email_token
from app.models import User
from app.models.consts import TokenTypes
from app.schemas import (
    AuthToken,
    ErrorMessage,
    NewPassword,
    PasswordResetRequest,
    TokenSchema,
    UserAuth,
)

router = APIRouter(
    prefix="/auth",
    responses={
        422: {"model": ErrorMessage, "description": "Bad data"},
        403: {"model": ErrorMessage, "description": "Unauthorized"},
    },
)


@router.post("/signup", response_model=User)
async def sign_up(payload: UserAuth) -> User:
    new_user = await crud_user.create_regular_user(payload)
    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenSchema:
    email = EmailStr(form_data.username)
    user = await crud_user.get_user_by_email(email=email)
    authenticated = await user.authenticate(email=email, password=form_data.password)
    if not user or not authenticated:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed",
        )

    tokens = TokenSchema(
        access_token=create_token(token_type=TokenTypes.ACCESS, subject=user.id),
        refresh_token=create_token(token_type=TokenTypes.REFRESH, subject=user.id),
    )

    return tokens


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    current_user: User = Depends(get_current_user_form_refresh_token),
) -> TokenSchema:
    tokens = TokenSchema(
        access_token=create_token(
            token_type=TokenTypes.ACCESS, subject=current_user.id
        ),
        refresh_token=create_token(
            token_type=TokenTypes.REFRESH, subject=current_user.id
        ),
    )
    return tokens


@router.post("/reset_request")
async def reset_password_request(payload: PasswordResetRequest) -> AuthToken:
    """w body email
    w response
        - na razie: tymczasowe hasło
        - docelowo -nic, wysłanie maila"""
    user = await crud_user.get_user_by_email(email=payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return create_token(token_type=TokenTypes.EMAIL, subject=payload.email)


@router.post("/password_reset", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    new_password: NewPassword, current_user: User = Depends(get_user_from_email_token)
):
    current_user.hashed_password = get_hashed_password(new_password.password)
    await current_user.save()
    return status.HTTP_204_NO_CONTENT
