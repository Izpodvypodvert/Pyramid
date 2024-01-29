from pydantic import UUID4
from app.utils.exceptions import UnauthorizedAccessException


class AuthorshipMixin:
    async def _check_user_is_author_or_admin(self, entity_id, user_id, is_admin):
        if is_admin:
            return
        entity = await self.get_by_id(entity_id)
        if entity.author_id != user_id:
            raise UnauthorizedAccessException("User is not the author of the entity")
