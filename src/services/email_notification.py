import asyncio
import json

from redis.asyncio.client import Redis
from redis.exceptions import ConnectionError, RedisError, TimeoutError
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_async_session
from enums.enums import QueueEnum, TaskStatusEnum
from repositories.task import TaskRepository
from services.redis_client import redis_client
from utils.logger import setup_logger

logger = setup_logger(__name__)


class EmailNotification:
    """
    Класс для обработки и отправки email-уведомлений из очереди Redis.
    """

    def __init__(self, client: Redis):
        """
        Инициализация с Redis-клиентом.

        :param client: Асинхронный Redis-клиент.
        """
        self.client = client

    async def run(self) -> None:
        """
        Основной цикл обработки очереди уведомлений.
        Получает задачи из очереди Redis, обновляет их статус и инициирует отправку.
        """
        session: AsyncSession = await get_async_session()
        repo = TaskRepository(session)

        while True:
            try:
                # Блокирующее извлечение задачи из очереди
                _, data = await self.client.brpop(QueueEnum.EMAIL)
                task = json.loads(data)

                # Отправка уведомления
                await self.send(task)

                # Обновление статуса задачи
                await repo.update_status(task["id"], TaskStatusEnum.SEND)

            except ConnectionError:
                logger.error("Redis: Ошибка подключения")
            except TimeoutError:
                logger.error("Redis: Истекло время ожидания ответа")
            except RedisError as e:
                logger.error(f"Redis: Ошибка — {e.args}")
            except Exception as e:
                logger.error(f"Неизвестная ошибка: {e.args} : {e.__class__}")

            await asyncio.sleep(1)  # Небольшая пауза для предотвращения перегрузки

    async def send(self, message: dict) -> None:
        """
        Метод-обработчик отправки email-сообщений.

        :param message: Словарь с данными уведомления.
        """
        try:
            # Здесь будет логика интеграции с email-сервисом (например, SMTP или сторонний API)
            logger.info(f"Отправка уведомления: {message}")
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления: {e.args} : {e.__class__}")


async def notification_run():
    email_notification = EmailNotification(client=redis_client)
    await email_notification.run()
