from sqlmodel import select

from app.courses.models import Course, Lesson, Step, Topic
from app.core.repository import SQLModelRepository
from app.utils.logger import db_query_logger


class CoursesBaseSQLModelRepository(SQLModelRepository):

    @db_query_logger()
    async def find_one_or_none(self, ignore_published_status=False, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        if not ignore_published_status:
            statement = statement.filter(self.model.is_published == True)
        result = await self.session.exec(statement)
        return result.first()

    @db_query_logger()
    async def find_all(self, ignore_published_status=False, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        if not ignore_published_status:
            statement = statement.filter(self.model.is_published == True)
        result = await self.session.exec(statement)
        return result.all()


class CourseRepository(CoursesBaseSQLModelRepository):
    model = Course


class TopicRepository(CoursesBaseSQLModelRepository):
    model = Topic


class LessonRepository(CoursesBaseSQLModelRepository):
    model = Lesson


class StepRepository(CoursesBaseSQLModelRepository):
    model = Step
