from sqlalchemy import String, Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

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
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)