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

    async def get_or_create_progress(self, **data):
        progress_entity = await self.find_one_or_none(
            user_id=data.get("user_id"),
            course_id=data.get("course_id"),
            lesson_id=data.get("lesson_id"),
            step_id=data.get("step_id"),
        )

        if progress_entity:
            return progress_entity

        return await self.insert_data(**data)
