from fastapi_users import schemas
from pydantic import UUID4


class UserRead(schemas.BaseUser[UUID4]):
    """Schema with basic user model fields (except password):
    id, email address, is_active, is_superuser, is_verified."""

    username: str
    is_author: bool


class UserCreate(schemas.BaseUserCreate):
    """Scheme for creating a user. Email and password must be transmitted.
    Any other fields passed in the user creation request will be ignored."""

    username: str


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating the user object. Contains all the basic fields of the user model (including the password).
    All fields are optional. If the request is sent by a regular user (and not a superuser), then the is_active, is_superuser fields,
    is_verified is excluded from the dataset: these three fields can only be changed by the superuser.
    """

    username: str | None = None
    is_author: bool | None = None
