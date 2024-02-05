from app.courses.models import Course, Lesson, Step, Topic
from app.utils.repository import SQLModelRepository


class CourseRepository(SQLModelRepository):
    model = Course


class TopicRepository(SQLModelRepository):
    model = Topic


class LessonRepository(SQLModelRepository):
    model = Lesson


class StepRepository(SQLModelRepository):
    model = Step
