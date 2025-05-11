from pydantic import BaseModel, EmailStr, constr



class UserBase(BaseModel):
    """
    Базовая модель пользователя.
    Содержит поля, общие для различных операций с пользователем.
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Модель для создания нового пользователя.
    Используется при регистрации. Требует ввод email и пароля.
    """
    password: str = constr(min_length=6)


class UserRead(UserBase):
    """
    Модель для чтения данных пользователя.
    Используется в ответах API. Возвращает id и email.
    """
    id: int

    class Config:
        orm_mode = True