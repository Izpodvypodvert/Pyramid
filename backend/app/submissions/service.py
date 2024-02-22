from app.utils.service import BaseService
from app.users.models import User


class SubmissionsService(BaseService):
    async def get_user_submissions_by_step_id(self, step_id: int, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_submissions_by_step_id(step_id, user)
