from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from schemas.pydantic.user import UserCreate
import logging
from .base_db_repo import BaseDatabaseRepository

logger = logging.getLogger(__name__)

class UserRepository(BaseDatabaseRepository[User]):
    """
    Репозиторий для работы с моделью User.
    Отвечает за операции с базой данных, связанные с пользователями.
    """

    def __init__(self, session) -> None:
        """
        Инициализация репозитория пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session = session
        print(self.session)
    async def create(self, user_data: UserCreate) -> User:
        """
        Создает нового пользователя в базе данных.

        Args:
            user_data (UserCreate): Данные для создания пользователя (из схемы Pydantic).

        Returns:
            User: Объект пользователя, сохранённый в БД.

        """


        user = User(**user_data.model_dump())
        return await self.add(user)