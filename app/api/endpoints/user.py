from fastapi import APIRouter, HTTPException, status, Depends

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

user_router = APIRouter()

user_router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

# предоставляет доступ к эндпоинту /register
# для регистрации нового пользователя;
user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)


# Нужно разместить в начале кода что бы срабатывала
# ошибка но пропадет deprecated
@user_router.delete(
    # Путь и тег полностью копируют параметры эндпоинта по умолчанию.
    '/users/{id}',
    tags=['users'],
    # Параметр, который показывает, что метод устарел.
    deprecated=True

)
def delete_user(
        id: str,
):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        # 405 ошибка - метод не разрешен.
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!"
    )


# предоставляет доступ к эндпоинтам управления пользователями
# (чтение из БД, удаление, обновление).
user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
