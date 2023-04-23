from enum import Enum

from app.config import settings


class TaskStatus(str, Enum):
    COMPLETED = "done"
    NOT_COMPLETED = "to_do"


class TokenTypes(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    EMAIL = "email"


TOKEN_MAP = {
    TokenTypes.ACCESS: {
        "secret": settings.secret_key_access,
        "expires": settings.access_token_expires,
    },
    TokenTypes.REFRESH: {
        "secret": settings.secret_key_refresh,
        "expires": settings.refresh_token_expires,
    },
    TokenTypes.EMAIL: {
        "secret": settings.secret_key_refresh,
        "expires": settings.email_token_expires,
    },
}
