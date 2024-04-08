from datetime import datetime
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
        step = await self._get_step(submission["step_id"])

        response = {"result": result, "is_correct": False}

        if step.step_kind == StepKind.CODING_TASK:
            response = await self._handle_coding_task(submission, step, result)

        elif step.step_kind == StepKind.THEORY:
            pass
        elif step.step_kind == StepKind.TEST:
            pass

        return response

    async def _get_step(self, step_id):
        async with self.transaction_manager:
            return await self.transaction_manager.step.find_one_or_none(
                ignore_published_status=True, id=step_id
            )

    async def _get_result_of_coding_task(self, submitted_answer: str) -> str:
        try:
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

    async def _handle_coding_task(
        self, submission: dict, step: Step, result: str
    ) -> dict:
        coding_task = step.coding_task
        is_correct = False

        if (
            coding_task.test_type == TestType.SIMPLE
            and result == coding_task.simple_test_expected_output
        ):
            is_correct = True
            submission.update({"is_correct": True})
            await self._update_user_progress(submission, step)

        elif coding_task.test_type == TestType.ADVANCED:
            pass

        return {"result": result, "is_correct": is_correct}
