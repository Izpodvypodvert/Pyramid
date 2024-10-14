
from pydantic import UUID4
from typing import  Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    UUIDIDMixin,
    InvalidPasswordException,
)
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_async_session
from app.users.models import User
from app.users.schemas import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLModelUserDatabaseAsync(session=session, user_model=User)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID4]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Password should be at least 3 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Method for actions after successful user registration."""
        print(f"The user {user.email} is registered.")
        
    
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
        