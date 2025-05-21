from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from enums.enums import TaskStatusEnum
from models.models import Task
from schemas.task import TaskCreate, TaskRead
from utils.logger import setup_logger

from .base_db_repo import BaseDatabaseRepository

logger = setup_logger(__name__)


class TaskRepository(BaseDatabaseRepository[Task]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model = Task

    async def create(self, task: TaskCreate):
        new_task = self.model(**task.model_dump())
        return await self.add(new_task)

    async def get_all_pending(self) -> list[TaskRead]:
        """
        Получает все задачи со статусом NEW или FAILED.
        Используется воркером для публикации в очередь.
        """
        try:
            smtm = select(self.model).where(
                self.model.status.in_([TaskStatusEnum.NEW, TaskStatusEnum.FAILED])
            )
            result = await self.session.execute(smtm)
            tasks = [
                TaskRead.model_validate(task).model_dump()
                for task in result.scalars().all()
            ]
            return tasks

        except SQLAlchemyError as e:
            logger.error(
                f"Произошла ошибка при получении списка задач: {e.args}:{e.__class__}"
            )

    async def update_status(self, task_id: int, status: TaskStatusEnum) -> None:
        try:
            await self.update(task_id, {"status": status})
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при обновлении статуса задачи: {e.args}: {e.__class__}"
            )
