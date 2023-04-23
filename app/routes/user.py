from fastapi import APIRouter, Depends
from pydantic import EmailStr

from app.crud import user as crud_user
from app.deps import get_current_user
from app.models import User
from app.schemas import ErrorMessage, UserRead

router = APIRouter(
    prefix="/users",
    responses={422: {"model": ErrorMessage, "description": "Bad data"}},
)


@router.get("/", response_model=UserRead)
async def get_user(email: EmailStr) -> UserRead:
    user = await crud_user.get_user_by_email(email)
    return UserRead(**user.dict())


@router.get("/me", response_model=UserRead)
async def get_self(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead(**current_user.dict())
