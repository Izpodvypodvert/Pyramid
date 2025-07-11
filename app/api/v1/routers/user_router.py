from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.exceptions import InvalidVerifyToken, UserAlreadyVerified

from app.users.auth_config import auth_backend, current_user, fastapi_users
from app.users.manager import UserManager, get_user_manager
from app.users.models import User
from app.users.schemas import UserCreate, UserRead, UserUpdate, VerifyEmailRequest

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


@router.post("/auth/verify-email", tags=["auth"])
async def verify_email(
    request: VerifyEmailRequest, user_manager: UserManager = Depends(get_user_manager)
):
    try:
        user = await user_manager.verify(request.token)
        return {"message": "Email успешно верифицирован"}
    except InvalidVerifyToken:
        raise HTTPException(status_code=400, detail="Неверный или истекший токен")
    except UserAlreadyVerified:
        raise HTTPException(status_code=400, detail="Пользователь уже верифицирован")


@router.post("/auth/request-verification")
async def request_verification(
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Пользователь уже верифицирован.")

    await user_manager.on_after_request_verify(user)

    return {"message": "Письмо для верификации отправлено повторно."}
