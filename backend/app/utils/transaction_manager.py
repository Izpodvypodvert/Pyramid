from abc import ABC, abstractmethod
from backend.app.core.db import get_async_session

from backend.app.courses.repository import CoursesRepository


class ITransactionManager(ABC):
    """Interface for implementing the UOW pattern
    for working with transactions to the database"""

    courses: CoursesRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class TransactionManager(ITransactionManager):
    """Implementation of the interface for working with transactions"""

    def __init__(self):
        self.session_factory = get_async_session

    async def __aenter__(self):
        self.session = self.session_factory()
        self.courses = CoursesRepository(self.session)

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
