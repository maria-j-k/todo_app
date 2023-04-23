from enum import Enum


class TaskStatus(str, Enum):
    COMPLETED = "done"
    NOT_COMPLETED = "to_do"


class TokenTypes(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
