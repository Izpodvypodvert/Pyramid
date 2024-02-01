from pydantic import UUID4
from app.utils.exceptions import UnauthorizedAccessException


class AuthorshipMixin:
    async def _check_user_is_author_or_admin(self, entity_id, user_id, is_admin):
        if is_admin:
            return True

        entity = await self.repository.find_one_or_none(
            id=entity_id, ignore_published_status=True
        )
        if not entity or entity.author_id != user_id:
            raise UnauthorizedAccessException("User is not the author of the entity")
        return True
