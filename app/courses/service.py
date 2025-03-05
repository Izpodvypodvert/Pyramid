from pydantic import UUID4
from sqlmodel import SQLModel
from app.courses.models import Topic, Lesson, Step
from app.core.service import BaseService
from app.utils.mixins import AuthorshipMixin
from app.users.models import User
from app.utils.exceptions import IncorrectIdException
from app.users.schemas import UserUpdate


class BaseServiceWithAuthorship[T](AuthorshipMixin, BaseService):
    """A basic service with support for checking administrator and author rights.
    Provides methods for getting, deleting, and updating entities based on user rights.
    Administrators can receive any entities, authors can receive their own entities and published ones,
    regular users are only published entities."""

    _PARENTS = {
        Topic: "course_id",
        Lesson: "topic_id",
        Step: "lesson_id",
    }

    async def get_all(self, user: User) -> list[T] | None:

        async with self.transaction_manager:
            if user.is_superuser:
                return await self.repository.find_all(ignore_published_status=True)

            if user.is_author:
                user_courses = await self.repository.find_all(
                    author_id=user.id, ignore_published_status=True
                )

                published_courses = await self.repository.find_all(is_published=True)

                return list(set(user_courses + published_courses))

            return await self.repository.find_all()

    async def get_all_by_id(self, user: User, parent_id: int) -> list[T] | None:
        field_name = self._PARENTS.get(self.entity_type)
        kwargs = {field_name: parent_id}
        async with self.transaction_manager:
            if user.is_superuser:
                return await self.repository.find_all(
                    ignore_published_status=True, **kwargs
                )

            if user.is_author:
                user_courses = await self.repository.find_all(
                    author_id=user.id, ignore_published_status=True, **kwargs
                )

                published_courses = await self.repository.find_all(
                    is_published=True, **kwargs
                )

                return list(set(user_courses + published_courses))

            return await self.repository.find_all(**kwargs)

    async def get_by_id(self, entity_id, user: User) -> T | None:
        async with self.transaction_manager:
            if await self._check_user_is_author_or_admin(
                entity_id, user.id, user.is_superuser
            ):
                entity = await self.repository.find_one_or_none(
                    id=entity_id, ignore_published_status=True
                )
            else:
                entity = await self.repository.find_one_or_none(id=entity_id)
            if not entity:
                raise IncorrectIdException(f"Incorrect {self.entity_type.__name__} id")
            return entity

    async def delete(self, item_id: int, user_id: UUID4, is_admin: bool = False) -> int:
        async with self.transaction_manager:
            await self._check_user_is_author_or_admin(item_id, user_id, is_admin)
            return await self.repository.delete(id=item_id)

    async def update(
        self,
        item_id: int,
        item: SQLModel,
        user_id: UUID4,
        is_admin: bool = False,
    ) -> int:
        async with self.transaction_manager:
            await self._check_user_is_author_or_admin(item_id, user_id, is_admin)
            updated_data = self.get_updated_data(item, is_admin)
            return await self.repository.update_fields_by_id(item_id, **updated_data)

    def get_updated_data(self, item, is_admin: bool) -> dict:
        updated_data = item.model_dump(exclude_unset=True)
        if not is_admin:
            updated_data.pop("is_published", None)
        return updated_data

    async def create(self, item: T, user: User) -> T:
        async with self.transaction_manager:
            data = item.model_dump()
            data["author_id"] = user.id
            created_item = await self.repository.insert_data(**data)

            if user and not user.is_author:
                full_user = await self.user_manager.get(user.id)
                if full_user:
                    user_update_data = UserUpdate(is_author=True)

                    await self.user_manager.update(
                        user_update_data, full_user, safe=True
                    )

            return created_item


class CoursesService(BaseServiceWithAuthorship): ...


class TopicsService(BaseServiceWithAuthorship): ...


class LessonsService(BaseServiceWithAuthorship): ...


class StepsService(BaseServiceWithAuthorship): ...
