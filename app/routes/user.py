from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from app.deps import get_current_user
from app.models import User
from app.schemas import ErrorMessage, UserRead

router = APIRouter(
    prefix="/users",
    responses={422: {"model": ErrorMessage, "description": "Bad data"}},
)


@router.get("/me", response_model=UserRead)
async def get_self(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead(**current_user.dict())


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: EmailStr, current_user: User = Depends(get_current_user)):
    await current_user.delete()
    return status.HTTP_204_NO_CONTENT
