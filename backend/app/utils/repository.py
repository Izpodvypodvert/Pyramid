from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Session, select, update, delete


from app.utils.logger import db_query_logger


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, session: Session):
        ...

    @abstractmethod
    async def find_one_or_none(self, **filter_by):
        ...

    @abstractmethod
    async def find_all(self, **filter_by):
        ...

    @abstractmethod
    async def insert_data(self, **data):
        ...

    @abstractmethod
    async def update_fields_by_id(self, entity_id, **data):
        ...

    @abstractmethod
    async def delete(self, **filter_by):
        ...


class SQLModelRepository(AbstractRepository):
    model: type[SQLModel] = None

    def __init__(self, session: Session):
        self.session = session

    @db_query_logger()
    async def find_one_or_none(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.exec(statement)
        return result.first()

    @db_query_logger()
    async def find_all(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.exec(statement)
        return result.all()

    @db_query_logger()
    async def insert_data(self, **data):
        entity = self.model(**data)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    @db_query_logger()
    async def update_fields_by_id(self, entity_id, **data):
        statement = update(self.model).where(self.model.id == entity_id).values(**data)
        result = await self.session.exec(statement)
        return result.rowcount

    @db_query_logger()
    async def delete(self, **filter_by):
        statement = delete(self.model).filter_by(**filter_by)
        result = await self.session.exec(statement)
        return result.rowcount
