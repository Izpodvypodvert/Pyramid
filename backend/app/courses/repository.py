from app.courses.models import Course, Lesson, Step, Topic
from app.utils.repository import SQLModelRepository


class CoursesRepository(SQLModelRepository):
    model = Course


class TopicsRepository(SQLModelRepository):
    model = Topic


class LessonsRepository(SQLModelRepository):
    model = Lesson


class StepsRepository(SQLModelRepository):
    model = Step
