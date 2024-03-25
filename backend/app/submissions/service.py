from app.submissions.schemas import SubmissionCreate
from app.tasks.submission_tasks import process_submission
from app.users.models import User
from app.utils.logger import main_logger
from app.utils.service import BaseService


class SubmissionsService(BaseService):
    async def get_user_submissions_by_step_id(self, step_id: int, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_submissions_by_step_id(step_id, user)

    async def create(self, submission: SubmissionCreate):
        try:
            result2 = process_submission.delay(submission["submitted_answer"]).get(timeout=3)
            main_logger.info(f'result2 is {result2}')
            return {"result": result2} 
        
        except Exception as e:
            return {"result": "The waiting time has been exceeded"}

        