from typing import Callable, Dict, Generator, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field

from app.models.enums import TaskStatus


class CustomEmailStr(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Dict):
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


class AuthToken(BaseModel):
    token: str
    token_type: str = "Bearer"


class TokenSchema(BaseModel):
    access_token: AuthToken
    refresh_token: AuthToken


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    email: EmailStr

    class Config:
        allow_population_by_field_name = True


class ErrorMessage(BaseModel):
    message: str
