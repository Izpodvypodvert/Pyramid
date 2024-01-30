from app.courses.models import Course, Lesson, Topic
from app.utils.repository import SQLModelRepository


class CoursesRepository(SQLModelRepository):
    model = Course


class TopicsRepository(SQLModelRepository):
    model = Topic


class LessonRepository(SQLModelRepository):
    model = Lesson
