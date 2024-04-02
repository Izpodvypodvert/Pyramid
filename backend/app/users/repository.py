from sqlmodel import select
from app.utils.repository import SQLModelRepository
from app.users.models import UserProgress


class UserProgressRepository(SQLModelRepository):
    model = UserProgress
