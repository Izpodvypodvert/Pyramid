from fastapi import APIRouter, HTTPException

from app.users.dependencies import auth_backend, fastapi_users
from app.users.schemas import UserCreate, UserUpdate, UserRead


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.delete("/users/{id}", tags=["users"], deprecated=True)
def delete_user(id: str):
    """Redefined the method of deleting a user so that no one, not even the superuser,
    could not send a request to delete the user.
    If necessary, the user can be deactivated is_active=False"""
    raise HTTPException(status_code=405, detail="Deleting users is forbidden!")
