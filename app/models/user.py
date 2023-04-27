from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import AnyUrl, BaseModel, EmailStr, Field

from app.utils.auth_utils import verify_password


class ExternalIdentifier(BaseModel):
    iss: AnyUrl
    sub: str


class User(Document):
    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    hashed_password: str
    external_identifier: Optional[ExternalIdentifier]
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def authenticate(cls, email: EmailStr, password: str) -> bool:
        user = await cls.find_one(cls.email == email)
        if not user or not verify_password(password, user.hashed_password):
            return False
        return True
