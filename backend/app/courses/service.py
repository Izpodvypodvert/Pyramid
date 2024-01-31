from pydantic import UUID4
from app.utils.service import BaseService
from app.courses.models import Course, Lesson, Topic
from app.utils.mixins import AuthorshipMixin


class CoursesService(AuthorshipMixin, BaseService[Course]):
    async def delete(
        self, course_id: int, user_id: UUID4, is_admin: bool = False
    ) -> int:
        await self._check_user_is_author_or_admin(course_id, user_id, is_admin)
        return await super().delete(course_id)

    async def update(
        self, course_id: int, course: Course, user_id: UUID4, is_admin: bool = False
    ) -> int:
        await self._check_user_is_author_or_admin(course_id, user_id, is_admin)
        updated_data = course.model_dump(exclude_unset=True)
        if not is_admin:
            updated_data.pop("is_published", None)
        return await super().update(course_id, **updated_data)


class TopicsService(AuthorshipMixin, BaseService[Course]):
    async def delete(
        self, topic_id: int, user_id: UUID4, is_admin: bool = False
    ) -> int:
        topic_to_delete = await self.get_by_id(topic_id)
        await self._check_user_is_author_or_admin(
            topic_to_delete.course_id, user_id, is_admin
        )
        return await super().delete(topic_id)

    async def update(
        self, topic_id: int, topic: Topic, user_id: UUID4, is_admin: bool = False
    ) -> int:
        await self._check_user_is_author_or_admin(topic.course_id, user_id, is_admin)
        updated_data = topic.model_dump(exclude_unset=True)
        if not is_admin:
            updated_data.pop("is_published", None)
        return await super().update(topic_id, **updated_data)


class LessonsService(AuthorshipMixin, BaseService[Course]):
    async def delete(
        self, lesson_id: int, user_id: UUID4, is_admin: bool = False
    ) -> int:
        await self._check_user_is_author_or_admin(lesson_id, user_id, is_admin)
        return await super().delete(lesson_id)

    async def update(
        self, lesson_id: int, lesson: Lesson, user_id: UUID4, is_admin: bool = False
    ) -> int:
        await self._check_user_is_author_or_admin(lesson_id, user_id, is_admin)
        updated_data = lesson.model_dump(exclude_unset=True)
        if not is_admin:
            updated_data.pop("is_published", None)
        return await super().update(lesson_id, **updated_data)
