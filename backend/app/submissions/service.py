from datetime import datetime
from typing import Optional
from app.submissions.schemas import SubmissionCreate
from app.steps.models import CodingTask, TestType
from app.tasks.submission_tasks import process_submission, process_submission_with_advanced_test_code
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

        step = await self._get_step(submission["step_id"])

        response = {"result": "", "is_correct": False}

        if step.step_kind == StepKind.CODING_TASK:
            response = await self._handle_coding_task(submission, step)

        elif step.step_kind == StepKind.TEST:
            pass

        elif step.step_kind == StepKind.THEORY:
            pass

        submission.update({"is_correct": response["is_correct"]})
        await self.repository.insert_data(**submission)

        return response

    async def _get_step(self, step_id):
        async with self.transaction_manager:
            return await self.transaction_manager.step.find_one_or_none(
                ignore_published_status=True, id=step_id
            )

    async def _get_result_of_coding_task(self, submitted_answer: str, advanced_test_code: str = "") -> str:
        try:
            if advanced_test_code:
                result: str = process_submission_with_advanced_test_code.delay(submitted_answer, advanced_test_code).get(timeout=3)
            else:
                result: str = process_submission.delay(submitted_answer).get(timeout=3)
            main_logger.info(f"result is {result}")
            return result

        except Exception as e:
            main_logger.info(f"Exception is  {e}")
            return "The waiting time has been exceeded"

    async def _update_user_progress(self, submission: dict, step: Step) -> None:
        await self.transaction_manager.userprogress.get_or_create_progress(
            user_id=submission["student_id"],
            course_id=step.course_id,
            lesson_id=step.lesson_id,
            step_id=step.id,
            is_completed=True,
            сompleted_at=datetime.now(),
        )

    async def _handle_coding_task(self, submission: dict, step: Step) -> dict:
        coding_task: CodingTask = step.coding_task
        main_logger.info(f"coding_task.advanced is {coding_task.advanced_test_code}")
        main_logger.info(
            f"coding_task.advanced is {coding_task.advanced_test_code == ""}"
        )
        is_correct = False

            
        if coding_task.test_type == TestType.SIMPLE:
            result = await self._get_result_of_coding_task(submission["submitted_answer"])
            
            if result == coding_task.simple_test_expected_output:  
                is_correct = True
                await self._update_user_progress(submission, step)

        elif coding_task.test_type == TestType.ADVANCED:
            result = await self._get_result_of_coding_task(submission["submitted_answer"], coding_task.advanced_test_code)
            if result.endswith("OK"):
                is_correct = True
            else:
                is_correct = False
        return {"result": result, "is_correct": is_correct}
