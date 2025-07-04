from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request
from fastapi_users.authentication import Strategy
from fastapi_users.exceptions import UserNotExists

from app.core.service import BaseService
from app.users.auth_config import auth_backend
from app.users.manager import UserManager
from app.users.models import User
from app.users.schemas import UserCreate


class UserProgressService(BaseService):
    async def get_user_steps_progress(self, lesson_id: int, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_steps_progress(lesson_id, user)

    async def get_user_lessons_progress(self, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_lessons_progress(user)


async def get_or_create_user(
    user_info: dict, user_manager: UserManager, is_verified: bool = False
) -> UserCreate:
    """Search for or create a user."""
    email = user_info.get("email")
    username = user_info.get("name")
    try:
        user = await user_manager.get_by_email(email)
    except UserNotExists:
        user_create = UserCreate(
            email=email,
            username=username,
            password="oauth_default_password",
            is_verified=is_verified,
        )
        user = await user_manager.create(user_create)
    return user


async def generate_access_token(user) -> str:
    """Generation of a JWT token."""
    auth_strategy: Strategy = auth_backend.get_strategy()
    return await auth_strategy.write_token(user)


async def get_google_user_info(request: Request, oauth_client: OAuth) -> dict:
    """Getting user data from Google."""
    data: dict = await oauth_client.google.authorize_access_token(request)
    user_info = data.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="No user info found")
    return user_info
