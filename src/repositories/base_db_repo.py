from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Callable

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager
T = TypeVar("T") # Тип модели ORM

class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, obj: T) -> T:
        ...

class BaseDatabaseRepository(IRepository[T]):
    def __init__(
            self,
            model: Type[T],
            session_factory:AsyncSession) -> None:
        self.model = model
        self.session = session_factory

    async def add(self, obj: T) -> T:

        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f"Ошибка SQLAlchemy при создании объекта модели : {e.__class__}: {e.args}")
            raise e
        except Exception as e:
            print(f"Неизвестная ошибка: {e.__class__}: {e.args}")
            raise e

