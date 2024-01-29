from fastapi import HTTPException, status
from pydantic import BaseModel


class OpenAPIDocExtraResponse(BaseModel):
    """Class for extra responses in OpenAPI doc"""

    detail: str


class AppException(HTTPException):
    """Base class for all courses exceptions"""

    def __init__(
        self, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, detail: str = ""
    ):
        super().__init__(status_code=status_code, detail=detail)


class IncorrectIdException(AppException):
    """Exception raised when an entity with a specific ID is not found."""

    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )


class UnauthorizedAccessException(AppException):
    """Exception raised when a user attempts to access an entity without authorization."""

    def __init__(self, message="User is not the author of the entity"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )
