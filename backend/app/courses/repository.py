from app.courses.models import Course
from app.utils.repository import SQLModelRepository


class CoursesRepository(SQLModelRepository):
    model = Course
