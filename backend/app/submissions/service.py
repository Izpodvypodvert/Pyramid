from app.utils.service import BaseService
from app.users.models import User
from app.submissions.schemas import SubmissionCreate
from app.tasks.submission_tasks import hello_world


class SubmissionsService(BaseService):
    async def get_user_submissions_by_step_id(self, step_id: int, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_submissions_by_step_id(step_id, user)

    async def create(self, submission: SubmissionCreate):
        try:
            result = hello_world.delay().get(timeout=3)
            print(result)
        except Exception as e:
            print(e)

        return {"result": "result"}  # result
