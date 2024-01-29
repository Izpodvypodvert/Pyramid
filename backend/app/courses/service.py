from pydantic import UUID4
from app.utils.service import BaseService
from app.courses.models import Course
from app.utils.mixins import AuthorshipMixin


class CoursesService(AuthorshipMixin, BaseService[Course]):
    async def delete(
        self, course_id: int, user_id: UUID4, is_admin: bool = False
    ) -> int:
        await self._check_user_is_author_or_admin(course_id, user_id, is_admin)
        return await super().delete(course_id)

    async def update(
        self, course: Course, user_id: UUID4, is_admin: bool = False
    ) -> int:
        await self._check_user_is_author_or_admin(course.id, user_id, is_admin)
        updated_data = course.model_dump()
        updated_data.pop("id", None)
        return await super().update(course.id, **updated_data)
