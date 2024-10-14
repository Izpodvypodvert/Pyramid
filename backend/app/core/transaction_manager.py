from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import async_session_maker
from app.courses.repository import (
    CourseRepository,
    LessonRepository,
    StepRepository,
    TopicRepository,
)
from app.steps.repository import (
    TheoryRepository,
    CodingTaskRepository,
    TestRepository,
    TestChoiceRepository,
)
from app.submissions.repository import SubmissionRepository
from app.users.repository import UserProgressRepository


class ITransactionManager(ABC):
    """Interface for implementing the UOW pattern
    for working with transactions to the database"""

    course: CourseRepository
    topic: TopicRepository
    lesson: LessonRepository
    step: StepRepository
    theory: TheoryRepository
    codingtask: CodingTaskRepository
    test: TestRepository
    testchoice: TestChoiceRepository
    submission: SubmissionRepository
    userprogress: UserProgressRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class TransactionManager(ITransactionManager):
    """Implementation of the interface for working with transactions"""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.course = CourseRepository(self.session)
        self.topic = TopicRepository(self.session)
        self.lesson = LessonRepository(self.session)
        self.step = StepRepository(self.session)

        self.theory = TheoryRepository(self.session)
        self.codingtask = CodingTaskRepository(self.session)
        self.test = TestRepository(self.session)
        self.testchoice = TestChoiceRepository(self.session)

        self.submission = SubmissionRepository(self.session)

        self.userprogress = UserProgressRepository(self.session)

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
