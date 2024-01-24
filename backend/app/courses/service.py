from backend.app.courses.exceptions import (
    IncorrectCourseIdException,
    UnauthorizedAccessCourseException,
)
from backend.app.courses.models import Course
from backend.app.utils.transaction_manager import ITransactionManager
from backend.app.utils.logger import services_logger


class CoursesService:
    @staticmethod
    async def get_courses(
        transaction_manager: ITransactionManager,
    ) -> list[Course] | None:
        async with transaction_manager:
            courses = await transaction_manager.courses.find_all()
            await transaction_manager.commit()
            return courses

    @staticmethod
    async def _get_course(
        transaction_manager: ITransactionManager,
        course_id: int,
        user_id: int,
    ) -> Course:
        course = await transaction_manager.courses.find_one_or_none(
            id=course_id, user_id=user_id
        )

        if not course:
            services_logger.warning(
                "Incorrect course id or user_id",
                extra={"user_id": user_id, "course_id": course_id},
            )
            raise IncorrectCourseIdException

        return course

    @staticmethod
    async def get_course(
        transaction_manager: ITransactionManager,
        course_id: int,
        user_id: int,
    ) -> Course | None:
        async with transaction_manager:
            course = await CoursesService._get_course(
                transaction_manager, course_id, user_id
            )

            await transaction_manager.commit()
            return course

    @staticmethod
    async def delete_course(
        transaction_manager: ITransactionManager,
        course_id: int,
        user_id: int,
    ) -> Course:
        async with transaction_manager:
            course_to_delete = await CoursesService._get_course(
                transaction_manager, course_id, user_id
            )

            if course_to_delete.author != user_id:
                services_logger.warning(
                    "Attempted to delete a course with incorrect user_id",
                    extra={"user_id": user_id, "course_id": course_id},
                )
                raise UnauthorizedAccessCourseException

            deleted_course = await transaction_manager.courses.delete(
                id=course_id, user_id=user_id
            )

            if not deleted_course:
                services_logger.warning(
                    "Incorrect course id or user_id",
                    extra={"user_id": user_id, "course_id": course_id},
                )
                raise IncorrectCourseIdException

            await transaction_manager.commit()
            return deleted_course

    @staticmethod
    async def add_course(
        transaction_manager: ITransactionManager, course_id: int, user_id: int
    ) -> Course:
        async with transaction_manager:
            course = await transaction_manager.courses.insert_data(
                id=course_id, user_id=user_id
            )
            await transaction_manager.commit()
            return course
