from pydantic import UUID4
from sqlmodel import SQLModel
from app.utils.service import BaseService
from app.utils.mixins import AuthorshipMixin


class BaseServiceWithAuthorship(AuthorshipMixin, BaseService):
    async def delete(self, item_id: int, user_id: UUID4, is_admin: bool = False) -> int:
        await self._check_user_is_author_or_admin(item_id, user_id, is_admin)
        return await super().delete(item_id)

    async def update(
        self,
        item_id: int,
        item: SQLModel,
        user_id: UUID4,
        is_admin: bool = False,
    ) -> int:
        await self._check_user_is_author_or_admin(item_id, user_id, is_admin)
        updated_data = self.get_updated_data(item, is_admin)
        return await super().update(item_id, **updated_data)

    def get_updated_data(self, item, is_admin: bool) -> dict:
        updated_data = item.model_dump(exclude_unset=True)
        if not is_admin:
            updated_data.pop("is_published", None)
        return updated_data


class CoursesService(BaseServiceWithAuthorship):
    ...


class TopicsService(BaseServiceWithAuthorship):
    ...


class LessonsService(BaseServiceWithAuthorship):
    ...


class StepsService(BaseServiceWithAuthorship):
    ...
