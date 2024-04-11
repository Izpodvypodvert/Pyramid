from datetime import datetime
import re
from typing import Optional
from app.submissions.schemas import SubmissionCreate
from app.steps.models import CodingTask, Test, TestType
from app.tasks.submission_tasks import (
    process_submission,
    process_submission_with_advanced_test_code,
)
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

        step: Step = await self._get_step(submission["step_id"])

        response = {"result": "", "is_correct": False}

        step_handlers = {
            StepKind.CODING_TASK: self._handle_coding_task,
            StepKind.TEST: self._handle_test,
            StepKind.THEORY: self._handle_theory,
        }

        if step.step_kind in step_handlers:
            response = await step_handlers[step.step_kind](submission, step)
        else:
            response["result"] = "Error: Unhandled step kind."

        submission.update({"is_correct": response["is_correct"]})
        await self.repository.insert_data(**submission)

        return response

    async def _get_step(self, step_id):
        async with self.transaction_manager:
            return await self.transaction_manager.step.find_one_or_none(
                ignore_published_status=True, id=step_id
            )

    async def _get_result_of_coding_task(
        self, submitted_answer: str, advanced_test_code: str = ""
    ) -> str:
        try:
            if advanced_test_code:
                result: str = process_submission_with_advanced_test_code.delay(
                    submitted_answer, advanced_test_code
                ).get(timeout=3)
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

    async def _handle_coding_task(
        self, submission: dict, step: Step
    ) -> dict[str, bool]:

        coding_task: CodingTask = step.coding_task

        if coding_task.test_type == TestType.SIMPLE:

            return await self._handle_simple_test(submission, coding_task, step)

        elif coding_task.test_type == TestType.ADVANCED:
            return await self._handle_advanced_test(submission, coding_task, step)

        return {"result": "Unknown CodingTask type", "is_correct": False}

    async def _handle_test(self, submission: dict, step: Step):
        correct_test_choice = next(
            (choice for choice in step.test.test_choices if choice.is_correct), None
        )

        if correct_test_choice is None:
            return {
                "result": "Error: Test configuration issue. Don't forget to set a correct TestChoice.",
                "is_correct": False,
            }

        is_correct = correct_test_choice.id == int(submission["submitted_answer"])
        if is_correct:
            await self._update_user_progress(submission, step)

        return {
            "result": "Correct answer!" if is_correct else "Incorrect answer.",
            "is_correct": is_correct,
        }

    async def _handle_theory(self, submission: dict, step: Step):
        await self._update_user_progress(submission, step)
        return {
            "result": "The theory has been successfully completed.",
            "is_correct": True,
        }

    async def _handle_simple_test(
        self, submission: dict, coding_task: CodingTask, step: Step
    ) -> dict[str, bool]:
        result = await self._get_result_of_coding_task(submission["submitted_answer"])
        if result == coding_task.simple_test_expected_output:
            await self._update_user_progress(submission, step)
            return {"result": result, "is_correct": True}
        return {"result": result, "is_correct": False}

    async def _handle_advanced_test(
        self, submission: dict, coding_task: CodingTask, step: Step
    ) -> dict[str, bool]:
        result = await self._get_result_of_coding_task(
            submission["submitted_answer"], coding_task.advanced_test_code
        )
        if result.endswith("OK"):
            await self._update_user_progress(submission, step)
            return {"result": "OK", "is_correct": True}

        return {"result": self._extract_error_or_exception(result), "is_correct": False}

    def _extract_error_or_exception(self, result: str) -> str:
        exception_pattern = r"(Exception: .+?)\n"
        error_pattern = r"(\w+Error: .+?)(\n|$)"
        pattern = rf"(?:{exception_pattern}|{error_pattern})"
        matches = re.findall(pattern, result)

        if not matches:
            return result.split("\n")[-1]
        else:
            return next((match for match in matches[0] if match), result)
