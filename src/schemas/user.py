from pydantic import BaseModel, ConfigDict, EmailStr, constr


class UserBase(BaseModel):
    """
    Базовая схема пользователя.
    Общие поля, используемые как при создании, так и при чтении данных пользователя.

    :param email: Адрес электронной почты пользователя.
    """

    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя (регистрация).

    :param password: Пароль пользователя (минимум 6 символов).
    """

    password: str = constr(min_length=6)


class UserRead(UserBase):
    """
    Схема для чтения информации о пользователе.

    :param id: Уникальный идентификатор пользователя.
    """

    id: int
