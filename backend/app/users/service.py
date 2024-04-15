from app.users.models import User
from app.utils.service import BaseService


class UserProgressService(BaseService):
    async def get_user_steps_progress(self, lesson_id: int, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_steps_progress(lesson_id, user)

    async def get_user_lessons_progress(self, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_lessons_progress(user)
