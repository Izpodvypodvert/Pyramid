from app.courses.exceptions import (
    IncorrectCourseIdException,
    UnauthorizedAccessCourseException,
)
from app.courses.models import Course
from app.utils.transaction_manager import ITransactionManager
from app.utils.logger import services_logger


class CoursesService:
    @staticmethod
    async def get_courses(
        transaction_manager: ITransactionManager,
    ) -> list[Course] | None:
        async with transaction_manager:
            courses = await transaction_manager.courses.find_all()

            return courses

    @staticmethod
    async def _get_course(
        transaction_manager: ITransactionManager,
        course_id: int,
    ) -> Course:
        course = await transaction_manager.courses.find_one_or_none(id=course_id)

        if not course:
            services_logger.warning(
                "Incorrect course id",
                extra={"course_id": course_id},
            )
            raise IncorrectCourseIdException

        return course

    @staticmethod
    async def get_course(
        transaction_manager: ITransactionManager,
        course_id: int,
    ) -> Course | None:
        async with transaction_manager:
            course = await CoursesService._get_course(transaction_manager, course_id)

            return course

    @staticmethod
    async def delete_course(
        transaction_manager: ITransactionManager,
        course_id: int,
        user_id: int,
    ) -> int:
        async with transaction_manager:
            course_to_delete = await CoursesService._get_course(
                transaction_manager, course_id
            )

            if course_to_delete.author_id != user_id:
                services_logger.warning(
                    "Attempted to delete a course with incorrect user_id",
                    extra={"user_id": user_id, "course_id": course_id},
                )
                raise UnauthorizedAccessCourseException

            deleted_course = await transaction_manager.courses.delete(
                id=course_id, author_id=user_id
            )

            if not deleted_course:
                services_logger.warning(
                    "Incorrect course id or user_id",
                    extra={"user_id": user_id, "course_id": course_id},
                )
                raise IncorrectCourseIdException

            return deleted_course

    @staticmethod
    async def create_course(
        course: Course, transaction_manager: ITransactionManager, user_id: int
    ) -> Course:
        async with transaction_manager:
            course = await transaction_manager.courses.insert_data(
                **course.model_dump(), user_id=user_id
            )
            return course
