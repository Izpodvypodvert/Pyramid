from typing import Optional
from app.submissions.schemas import SubmissionCreate
from app.steps.models import TestType
from app.tasks.submission_tasks import process_submission
from app.users.models import User
from app.utils.logger import main_logger
from app.utils.service import BaseService
from app.courses.models import Step, StepKind
from app.utils.transaction_manager import TransactionManager


class SubmissionsService(BaseService):
    async def get_user_submissions_by_step_id(self, step_id: int, user: User):
        async with self.transaction_manager:
            return await self.repository.get_user_submissions_by_step_id(step_id, user)

    async def create(self, submission: dict):

        result: str = await self._get_result_of_coding_task(
            submission["submitted_answer"]
        )
        response = {"result": result, "is_correct": False}
        async with self.transaction_manager:
            step = await self.transaction_manager.step.find_one_or_none(
                ignore_published_status=True, id=submission["step_id"]
            )
            main_logger.info(step)
            if step.step_kind == StepKind.CODING_TASK:
                coding_task = step.coding_task
                main_logger.info(coding_task)
                if coding_task.test_type == TestType.SIMPLE:
                    main_logger.info(
                        f"coding_task.simple_test_expected_output is {coding_task.simple_test_expected_output}"
                    )
                    main_logger.info(f"and result is {result}")
                    if result == coding_task.simple_test_expected_output:
                        submission.update({"is_correct": True})
                        response.update({"is_correct": True})
                        # так же нужно добавить создание объекта UserProgress с полем is_completed = True
                        # для этого нужно сделать соответствующий сервис и репозиторий в модуле course

                        await self.transaction_manager.userprogress.insert_data(
                            course_id=step.course_id,
                            lesson_id=step.lesson_id,
                            step_id=step.id,
                            is_completed=True,
                        )
                    await self.repository.insert_data(**submission)

        return response

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

    async def _get_result_of_coding_task(self, submitted_answer: str) -> str:
        try:
            result: str = process_submission.delay(submitted_answer).get(timeout=3)
            main_logger.info(f"result is {result}")
            return result

        except Exception as e:
            main_logger.info(f"Exception is  {e}")
            return "The waiting time has been exceeded"
