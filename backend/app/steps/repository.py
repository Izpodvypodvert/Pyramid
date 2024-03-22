from app.utils.repository import SQLModelRepository
from app.steps.models import Theory, CodingTask, Test, TestChoice


class TheoryRepository(SQLModelRepository):
    model = Theory


class CodingTaskRepository(SQLModelRepository):
    model = CodingTask


class TestRepository(SQLModelRepository):
    model = Test


class TestChoiceRepository(SQLModelRepository):
    model = TestChoice
