from sqlmodel import SQLModel

from app.core.service import BaseService
from app.steps.models import Theory, CodingTask, Test, TestChoice
from app.users.models import User



class StepsRelatedBaseService[T](BaseService):
    _PARENTS = {
        Theory: "step_id",
        CodingTask: "step_id",
        Test: "step_id",
        TestChoice: "test_id",
    }

    async def get_all(self, user: User) -> list[T] | None:
        return await super().get_all()

    async def get_by_id(self, entity_id, user: User) -> T | None:
        return await super().get_by_id(entity_id)

    async def create(self, item: T, user: User) -> T:
        return await super().create(item)

    async def delete(self, item_id: int, user: User) -> int:
        return await super().delete(item_id)

    async def update(self, item_id: int, item: SQLModel, user: User) -> int:
        return await super().update(item_id, item)

    async def get_all_by_id(self, user: User, parent_id: int) -> list[T] | None:
        field_name = self._PARENTS.get(self.entity_type)
        kwargs = {field_name: parent_id}
        async with self.transaction_manager:
            return await self.repository.find_all(**kwargs)


class TheoriesService(StepsRelatedBaseService): ...


class CodingTasksService(StepsRelatedBaseService): ...


class TestsService(StepsRelatedBaseService): ...


class TestChoicesService(StepsRelatedBaseService): ...
