from fastapi import HTTPException, status


class CourseAppException(HTTPException):
    """Base class for all courses exceptions"""

    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectCourseIdException(CourseAppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Booking with this id was not found"


class UnauthorizedAccessCourseException(CourseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized access to the course"
