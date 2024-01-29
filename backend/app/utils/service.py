from typing import Type

from app.utils.transaction_manager import ITransactionManager
from app.utils.exceptions import IncorrectIdException


class BaseService[T]:
    def __init__(self, entity_type: Type[T], transaction_manager: ITransactionManager):
        self.entity_type = entity_type
        self.transaction_manager = transaction_manager

    async def get_all(self) -> list[T] | None:
        async with self.transaction_manager:
            repository = getattr(
                self.transaction_manager, f"{self.entity_type.__name__.lower()}s"
            )
            return await repository.find_all()

    async def get_by_id(self, entity_id) -> T | None:
        async with self.transaction_manager:
            repository = getattr(
                self.transaction_manager, f"{self.entity_type.__name__.lower()}s"
            )
            entity = await repository.find_one_or_none(id=entity_id)
            if not entity:
                raise IncorrectIdException(f"Incorrect {self.entity_type.__name__} id")
            return entity

    async def create(self, entity: T) -> T:
        async with self.transaction_manager:
            repository = getattr(
                self.transaction_manager, f"{self.entity_type.__name__.lower()}s"
            )
            return await repository.insert_data(**entity.model_dump())

    async def delete(self, entity_id: int) -> int:
        async with self.transaction_manager:
            repository = getattr(
                self.transaction_manager, f"{self.entity_type.__name__.lower()}s"
            )
            return await repository.delete(id=entity_id)

    async def update(self, entity_id, **data) -> int:
        async with self.transaction_manager:
            repository = getattr(
                self.transaction_manager, f"{self.entity_type.__name__.lower()}s"
            )
            return await repository.update_fields_by_id(entity_id, **data)
