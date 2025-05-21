from pathlib import Path

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.logger import setup_logger

logger = setup_logger(__name__)

# Флаг для переключения между продакшен и дев-средой
PRODUCTION = False

# Базовая дериктория
BASE_DIR = Path(__file__).parent.parent

# Имя файла окружения
ENV_FILE = ".env.prod" if PRODUCTION else ".env.dev"
ENV_FILE_PATH = str(BASE_DIR.joinpath(ENV_FILE))


class Settings(BaseSettings):
    """
    Класс настроек приложения, загружающий переменные из .env-файла.

    Параметры:
        - PSQL_*: Настройки подключения к PostgreSQL.
        - REDIS_*: Настройки подключения к Redis.
        - JWT: Настройки генерации и верификации токенов.
        - FAST_API_*: Настройки FastAPI
    """

    PSQL_DB: str
    PSQL_USER: str
    PSQL_PASS: str
    PSQL_PORT: str
    PSQL_HOST: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    # FastAPI
    FAST_API_HOST: str
    FAST_API_PORT: int

    # Конфигурация загрузки из env-файла
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)

    def get_psql_async_connect_url(self) -> str:
        """
        Возвращает асинхронную строку подключения к PostgreSQL.
        """
        return f"postgresql+asyncpg://{self.PSQL_USER}:{self.PSQL_PASS}@{self.PSQL_HOST}:{self.PSQL_PORT}/{self.PSQL_DB}"

    def get_redis_connect_url(self) -> str:
        """
        Возвращает строку подключения к Redis.
        """
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


try:
    settings: Settings = Settings()
except ValidationError as e:
    logger.error(f"Ошибка валидации конфигурации: {e}")
    raise
