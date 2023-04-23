from __future__ import annotations

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, Link
from pydantic import Field

from app.models.enums import TaskStatus
from app.models.user import User


class Task(Document):
    title: Indexed(str, unique=True)  # type: ignore[valid-type]
    description: str
    status: Optional[TaskStatus] = TaskStatus.NOT_COMPLETED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: Link[User]
