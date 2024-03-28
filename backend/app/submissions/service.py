from app.submissions.schemas import SubmissionCreate
from app.tasks.submission_tasks import process_submission
from app.users.models import User
from app.utils.logger import main_logger
from app.utils.service import BaseService
from app.courses.models import StepKind


class SubmissionsService(BaseService):
    async def get_user_submissions_by_step_id(self, step_id: int, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_submissions_by_step_id(step_id, user)

    async def create(self, submission: SubmissionCreate):
        async with self.transaction_manager as tm:
            step = await tm.step.find_one_or_none(
                ignore_published_status=True, id=submission.step_id
            )
            main_logger.info(step)
            if step.step_kind == StepKind.CODING_TASK:
                pass
        try:
            # получить степ по step_id
            # определить является ли степ CodingTask StepKind.CODING_TASK
            # определить какой тип у CodingTask
            # если Simple то проверить что result == CodingTask.simple_test_expected_output
            # если Advanced то записать в файл solution_code и advanced_test_code: тесты проходят вернуть успех, в обратном случае вернуть ошибку
            # в случает правльного ответа нужно поставить Submission.is_correct = True и нужно указывать это в json

            result = process_submission.delay(submission["submitted_answer"]).get(
                timeout=3
            )
            main_logger.info(f"result is {result}")
            return {"result": result}

        except Exception as e:
            main_logger.info(f"Exception is  {e}")
            return {"result": "The waiting time has been exceeded"}

    async def create_old(self, submission: SubmissionCreate):
        try:
            result = process_submission.delay(submission["submitted_answer"]).get(
                timeout=3
            )
            main_logger.info(f"result is {result}")
            return {"result": result}

        except Exception as e:
            main_logger.info(f"Exception is  {e}")
            return {"result": "The waiting time has been exceeded"}
