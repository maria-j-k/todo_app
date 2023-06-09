from fastapi import HTTPException, status
from pydantic import AnyUrl, EmailStr

from app.models import ExternalIdentifier, User
from app.schemas import UserAuth
from app.utils.auth_utils import generate_temporary_password, get_hashed_password


async def create_regular_user(user_data: UserAuth) -> User:
    user = await get_user_by_email(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists",
        )

    new_user = User(
        email=user_data.email,
        hashed_password=get_hashed_password(user_data.password),
    )
    user = await new_user.insert()
    return user


async def get_user_by_email(email: EmailStr) -> User:
    user = await User.find_one(User.email == email)
    return user


async def create_social_user(email: EmailStr, iss: AnyUrl, sub: str) -> User:
    new_user = User(
        email=email,
        hashed_password=get_hashed_password(generate_temporary_password()),
        external_identifier=ExternalIdentifier(iss=iss, sub=sub),
    )
    user = await new_user.insert()
    return user
