import datetime

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from enums.enums import TaskStatusEnum


class Base(DeclarativeBase):
    """Базовый класс от которого наследуются все модели"""

    pass


class User(Base):
    """
    Модель для таблицы "users".
    Хранит информацию о пользователях.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    status: Mapped[TaskStatusEnum] = mapped_column(
        Enum(TaskStatusEnum, native_enum=False), nullable=False
    )
    data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=False
    )
