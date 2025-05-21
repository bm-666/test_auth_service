from sqlalchemy import select

from models.models import User
from schemas.user import UserCreate, UserRead
from utils.logger import setup_logger

from .base_db_repo import BaseDatabaseRepository

logger = setup_logger(__name__)


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

    async def create(self, user_data: UserCreate) -> UserRead | None:
        """
        Создает нового пользователя в базе данных.

        Args:
            user_data (UserCreate): Данные для создания пользователя (из схемы Pydantic).

        Returns:
            User: Объект пользователя, сохранённый в БД.

        """

        user = User(**user_data.model_dump())
        return await self.add(user)

    async def get_by_email(self, email) -> User | None:
        try:
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Ошибка при поиске пользователя:{e.args} : {e.__class__}")
            raise
