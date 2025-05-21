import asyncio
import json

from redis.asyncio.client import Redis

from database.session import get_async_session
from enums.enums import QueueEnum, TaskStatusEnum
from repositories.task import TaskRepository
from services.redis_client import redis_client
from utils.logger import setup_logger

logger = setup_logger(__name__)


class WorkerNotification:
    """
    Класс для обработки и отправки задач из базы данных в очередь Redis.
    """

    def __init__(self, client: Redis) -> None:
        """
        Инициализация воркера с Redis-клиентом.

        :param client: Асинхронный клиент Redis.
        """
        self.client = client

    async def dispatch_tasks(self):
        """
        Извлекает задачи со статусом PENDING и отправляет их в Redis очередь.
        После успешной отправки обновляет статус задачи.
        """
        session = await get_async_session()
        task_repo = TaskRepository(session)
        logger.info("Запуск процесса отправки задач")
        while True:

            tasks = await task_repo.get_all_pending()
            for task in tasks:
                data = json.dumps(task)

                try:
                    await self.client.lpush(QueueEnum.EMAIL, data)
                    await task_repo.update_status(task["id"], TaskStatusEnum.SEND)

                except Exception as e:
                    logger.error(f"fОшибка отправки задачи: {e} : {e.__class__}")

                    await session.close()
                    await task_repo.update_status(task["id"], TaskStatusEnum.FAILED)

            await asyncio.sleep(3)


async def worker_run():
    worker = WorkerNotification(client=redis_client)
    await worker.dispatch_tasks()
