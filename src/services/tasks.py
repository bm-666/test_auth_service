from sqlalchemy.ext.asyncio import AsyncSession

from custom_types.types import TaskSchema
from models.models import Task
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TaskPublish:
    """
    Сервисный класс для публикации задачи в базу данных.
    """

    def __init__(self, task: TaskSchema, session: AsyncSession) -> None:
        """
        Инициализация TaskPublisher.

        :param task: Объект задачи, которую необходимо сохранить.
        :param session: Асинхронная сессия SQLAlchemy.
        """
        self.task = task
        self.session = session

    async def publish_to_db(self) -> None:
        """
        Сохраняет задачу в базу данных.

        :raises SQLAlchemyError: В случае ошибки при сохранении задачи.
        """
        try:
            new_task = Task(**self.task.model_dump())
            self.session.add(new_task)
            await self.session.commit()
        except Exception as e:
            logger.error(f"Ошибка при сохранени задачи: {e.args} - {e.__class__}")
