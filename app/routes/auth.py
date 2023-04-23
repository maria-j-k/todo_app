from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.auth_utils import create_access_token, create_refresh_token
from app.crud import user as crud_user
from app.deps import get_current_user_form_refresh_token
from app.models import User
from app.schemas import ErrorMessage, TokenSchema, UserAuth

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
    if not user or not user.authenticate(email=email, password=form_data.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed",
        )

    tokens = TokenSchema(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )

    return tokens


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    current_user: User = Depends(get_current_user_form_refresh_token),
) -> TokenSchema:
    tokens = TokenSchema(
        access_token=create_access_token(current_user.id),
        refresh_token=create_refresh_token(current_user.id),
    )
    return tokens
