from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from app.core.db import AsyncSessionLocal as async_session_maker

from app.courses.repository import CoursesRepository, LessonRepository, TopicsRepository


class ITransactionManager(ABC):
    """Interface for implementing the UOW pattern
    for working with transactions to the database"""

    courses: CoursesRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class TransactionManager(ITransactionManager):
    """Implementation of the interface for working with transactions"""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.courses = CoursesRepository(self.session)
        self.topics = TopicsRepository(self.session)
        self.lessons = LessonRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


def get_transaction_manager(session_factory) -> ITransactionManager:
    return TransactionManager(session_factory)


# return a Unit of work instance for working with Session
TManagerDep = Annotated[
    ITransactionManager,
    Depends(lambda: get_transaction_manager(async_session_maker)),
]
