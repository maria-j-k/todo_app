from datetime import datetime
from enum import Enum
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class TaskStatus(str, Enum):
    COMPLETED = "done"
    NOT_COMPLETED = "to_do"


class Task(Document):
    title: Indexed(str, unique=True)  # type: ignore[valid-type]
    description: str
    status: Optional[TaskStatus] = TaskStatus.NOT_COMPLETED
    created_at: datetime = Field(default_factory=datetime.utcnow)
