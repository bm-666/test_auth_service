from sqlalchemy.ext.asyncio import AsyncSession

from custom_exceptions.exceptions import AuthenticationError, UserAlreadyExists
from custom_types.types import EmailNotificationTask
from enums.enums import EmailSubjectEnum
from models.models import User
from repositories.task import TaskRepository
from repositories.user import UserRepository
from schemas.jwt_token import TokenSchema
from schemas.task import TaskCreate
from schemas.user import UserCreate
from utils.logger import setup_logger
from utils.password import hash_password, verify_password
from utils.token import create_jwt_token

logger = setup_logger(__name__)


class AuthService:
    """
    Сервис аутентификации и регистрации пользователей.
    Отвечает за бизнес-логику, связанную с пользователями.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация сервиса с асинхронной сессией БД.

        :param session: Асинхронная SQLAlchemy-сессия.
        """
        self.session = session
        self.user_repo = UserRepository(session)
        self.task_repo = TaskRepository(session)

    async def register_user(self, user_data: UserCreate) -> User:
        """
        Регистрирует нового пользователя, хэширует пароль и создает задачу на отправку email-уведомления.
        :param user_data: Данные для регистрации пользователя.
        :raises UserAlreadyExists: Если пользователь с таким email уже существует.
        :raises EmailNotificationError: При ошибке создания уведомления.
        :return: Созданный пользователь.
        """

        if await self.user_repo.get_by_email(email=user_data.email):
            raise UserAlreadyExists()
        user_data.password = hash_password(user_data.password)
        user = await self.user_repo.create(user_data)
        try:
            notification = EmailNotificationTask(
                to=user.email,
                subject=EmailSubjectEnum.REGISTRATION,
                body=f"Hello {user.email}",
            )
            task = TaskCreate(data=notification.model_dump())
        except Exception as e:
            logger.error(f"Ошибка при создании уведомления: {str(e)}")

        await self.task_repo.create(task)

        return user

    async def authenticate_user(self, email: str, password: str) -> TokenSchema:
        user = await self.user_repo.get_by_email(email=email)
        if not user:
            raise AuthenticationError()
        if not verify_password(password, user.password):
            raise AuthenticationError()

        return await create_jwt_token(email=user.email)
