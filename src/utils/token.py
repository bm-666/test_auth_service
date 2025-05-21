from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from config.settings import settings
from custom_exceptions.exceptions import UnauthorizedException
from schemas.jwt_token import TokenSchema
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def create_jwt_token(
    email: str, expires_delta: timedelta | None = None
) -> TokenSchema:
    """
    Генерирует JWT токен на основе email пользователя.

    :param email: Email пользователя, используемый как subject (`sub`)
    :param expires_delta: Время жизни токена. Если не указано, используется значение по умолчанию из настроек
    :return: JWT токен, обёрнутый в схему TokenSchema
    """

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    )

    payload = {"sub": email, "exp": int(expire.timestamp())}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return TokenSchema(access_token=token, token_type="Bearer")


async def verify_jwt_token(token: str) -> dict[str, Any]:
    """
    Проверяет и декодирует JWT токен.
        :param token: Строка JWT токена
        :return: Раскодированные данные токена
        :raises UnauthorizedException: Если токен недействителен или подпись неверна
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.error(f"Ошибка декодирования токена: {e.args}")
        raise UnauthorizedException("Неверный токен")
