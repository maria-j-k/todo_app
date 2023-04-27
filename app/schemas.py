from typing import Callable, Dict, Generator, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, validator

from app.models.consts import TaskStatus
from app.utils.validators import password_is_valid


class CustomEmailStr(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Dict) -> EmailStr:
        return EmailStr(value["email"])


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskRead(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    title: str
    description: str
    status: TaskStatus
    user: CustomEmailStr

    class Config:
        allow_population_by_field_name = True


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class UserAuth(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def valid_password(cls, v):
        if not password_is_valid(v):
            raise ValueError("Password is too weak")
        return v


class UserRead(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    email: EmailStr

    class Config:
        allow_population_by_field_name = True


class PasswordResetRequest(BaseModel):
    email: EmailStr


class NewPassword(BaseModel):
    password: str

    @validator("password")
    def valid_password(cls, v):
        if not password_is_valid(v):
            raise ValueError("Password is too weak")
        return v


class ErrorMessage(BaseModel):
    message: str
