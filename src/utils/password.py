from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хеширует переданный пароль с использованием bcrypt.

    :param password: Обычный пароль в виде строки.
    :return: Хешированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Сравнивает обычный пароль с его хешированной версией.

    :param password: Введённый пользователем пароль.
    :param hashed_password: Ранее хешированный пароль из базы данных.
    :return: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(password, hashed_password)
