from enums.enums import ResponseCodeEnum


class BaseAppException(Exception):
    """
    Базовое приложение исключений, от которого наследуются все кастомные исключения.

    :param detail: Текстовое описание ошибки.
    """

    code: ResponseCodeEnum
    numeric_code: int
    detail: str

    def __init__(self, detail: str) -> None:
        self.detail = detail


class UserAlreadyExists(BaseAppException):
    """
    Исключение, возникающее при попытке создать пользователя с уже существующим email.
    """

    code = ResponseCodeEnum.USER_ALREADY_EXISTS
    numeric_code = 400

    def __init__(self) -> None:
        super().__init__("Пользователь с данным email уже зарегестрирован ранее")


class UserNotFound(BaseAppException):
    """
    Исключение, возникающее при попытке получить несуществующего пользователя.
    """

    code = ResponseCodeEnum.USER_NOT_FOUND
    numeric_code = 404
    # def __init__(self) -> None:
    #    super().__init__("Пользователь не зарегестрирован")


class InternalServerError(BaseAppException):
    """
    Исключение, указывающее на внутреннюю ошибку сервера.
    """

    code = ResponseCodeEnum.INTERNAL_SERVER_ERROR
    numeric_code = 500

    def __init__(self) -> None:
        super().__init__("Ошибка сервера")


class NotificationError(Exception):
    """
    Базовое исключение для ошибок при работе с уведомлениями.
    """

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)


class EmailNotificationError(NotificationError):
    """
    Ошибка, связанная с отправкой или созданием email-уведомления.
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class AuthenticationError(BaseAppException):
    """
    Исключение, возникающее при неверных учётных данных.
    """

    code = ResponseCodeEnum.AUTHENTICATION_ERROR
    numeric_code = 401

    def __init__(self):
        super().__init__("Неверный логин или пароль")


class UnauthorizedException(BaseAppException):
    """
    Исключение, возникающее при отсутствии авторизации или недействительном токене.
    """

    code = ResponseCodeEnum.UNAUTHORIZED_EXCEPTION
    numeric_code = 401

    def __init__(self, detail):
        super().__init__(detail)
