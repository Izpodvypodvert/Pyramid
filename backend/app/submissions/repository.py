from sqlmodel import select

from app.core.repository import SQLModelRepository
from app.submissions.models import Submission
from app.users.models import User


class SubmissionRepository(SQLModelRepository):
    model = Submission

    async def get_user_submissions_by_step_id(
        self, step_id: int, user: User
    ) -> list[Submission]:
        statement = select(self.model).where(
            self.model.step_id == step_id, self.model.student_id == user.id
        )
        submissions = await self.session.exec(statement)

        return submissions.all()
