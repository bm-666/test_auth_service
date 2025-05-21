from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from custom_exceptions.exceptions import UnauthorizedException, UserNotFound
from database.session import get_async_session
from repositories.user import UserRepository
from schemas.user import UserRead
from utils.logger import setup_logger
from utils.token import verify_jwt_token

logger = setup_logger(__name__)
# Инициализация схемы авторизации по заголовку Authorization: Bearer <token>
http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_async_session),
) -> UserRead:
    """
    Извлекает текущего пользователя из JWT токена, переданного в заголовке Authorization.

    :param credentials: Учётные данные из заголовка Authorization (тип Bearer).
    :param session: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
    :raises UnauthorizedException: Если токен недействителен или повреждён.
    :raises UserNotFound: Если пользователь с указанным email не найден.
    :return: Объект пользователя (схема UserRead), извлечённый из базы данных.
    """

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException("Токен не предоставлен")

    # Извлекаем токен из заголовка
    token = credentials.credentials

    # Провереям валидность токена
    try:
        payload = await verify_jwt_token(token)
    except JWTError:
        logger.error("Неверный токен")
        raise UnauthorizedException("Неверный токен")

    # Получаем пользователя из базы данных по email из payload
    user_repo = UserRepository(session)
    user = await user_repo.get_by_email(payload.get("sub"))
    if not user:
        raise UserNotFound("Пользователь не найден")
    return user
