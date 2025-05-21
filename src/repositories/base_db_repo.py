from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logger import setup_logger

logger = setup_logger(__name__)

T = TypeVar("T")  # Тип модели ORM


class IRepository(ABC, Generic[T]):
    """
    Абстрактный интерфейс репозитория.
    """

    @abstractmethod
    async def add(self, obj: T) -> T:
        """Добавление объекта в базу данных."""
        ...

    @abstractmethod
    async def update(self, obj: T, data: T) -> T | None:
        """Обновление объекта по ID"""
        ...


class BaseDatabaseRepository(IRepository[T]):
    """
    Базовая реализация репозитория для работы с базой данных через SQLAlchemy.

    :param model: ORM-модель, с которой работает репозиторий.
    :param session_factory: Асинхронная сессия SQLAlchemy.
    """

    def __init__(self, model: Type[T], session_factory: AsyncSession) -> None:
        self.model = model
        self.session = session_factory

    async def add(self, obj: T) -> T:
        """
        Добавляет объект в базу данных.

        :param obj: Экземпляр ORM-модели.
        :return: Сохранённый объект.
        """
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                f"Ошибка SQLAlchemy при создании объекта модели : {e.__class__}: {e.args}"
            )
            raise
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e.__class__}: {e.args}")
            raise

    async def update(self, obj_id: int, values: dict) -> None:
        """
        Обновляет объект по ID, используя переданные значения.

        :param obj_id: Идентификатор объекта.
        :param values: Словарь с новыми значениями для полей.
        """
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**values)
            .execution_options(synhronize_session="fetch")
        )
        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка обновления:{e.args}:{e.__class__}")
            pass
