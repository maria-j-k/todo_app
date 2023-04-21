from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.models import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskRead(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    title: str
    description: str
    status: TaskStatus

    class Config:
        allow_population_by_field_name = True


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]


class ErrorMessage(BaseModel):
    message: str
