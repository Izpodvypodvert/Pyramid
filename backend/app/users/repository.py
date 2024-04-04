from sqlmodel import select
from app.utils.repository import SQLModelRepository
from app.users.models import ProgressType, User, UserProgress


class UserProgressRepository(SQLModelRepository):
    model = UserProgress

    async def get_user_steps_progress(
        self, lesson_id: int, user: User
    ) -> list[UserProgress]:
        statement = select(self.model).where(
            self.model.lesson_id == lesson_id, self.model.user_id == user.id
        )
        progress = await self.session.exec(statement)

        return progress.all()

    async def get_user_lessons_progress(self, user: User) -> list[UserProgress]:
        statement = select(self.model).where(
            self.model.user_id == user.id,
            self.model.progress_type == ProgressType.LESSON,
        )
        progress = await self.session.exec(statement)
        return progress.all()
