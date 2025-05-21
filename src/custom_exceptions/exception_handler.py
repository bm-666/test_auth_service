from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHttpException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from custom_types.types import ErrorResponseSchema
from enums.enums import ResponseCodeEnum

from .exceptions import BaseAppException


def init_exception_handlers(app: FastAPI):
    """
    Регистрирует обработчики исключений для FastAPI-приложения.

    :param app: Экземпляр FastAPI.
    """

    @app.exception_handler(BaseAppException)
    async def app_exception_handler(request: Request, exc: BaseAppException):
        """
        Обработчик пользовательских исключений BaseAppException.

        :param request: Объект запроса.
        :param exc: Исключение BaseAppException.
        :return: JSON-ответ с детализированной ошибкой.
        """
        return JSONResponse(
            status_code=exc.numeric_code,
            content=ErrorResponseSchema(
                code=exc.code, numeric_code=exc.numeric_code, detail=exc.detail
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        Обработчик исключений валидации данных запроса.

        :param request: Объект запроса.
        :param exc: Исключение RequestValidationError.
        :return: JSON-ответ с информацией об ошибке валидации.
        """
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content=ErrorResponseSchema(
                code=ResponseCodeEnum.VALIDATION_ERROR,
                numeric_code=HTTP_400_BAD_REQUEST,
                detail="Ошибка валидации",
            ).model_dump(),
        )

    @app.exception_handler(StarletteHttpException)
    async def http_exception_handler(request: Request, exc: StarletteHttpException):
        """
        Обработчик стандартных HTTP-исключений.

        :param request: Объект запроса.
        :param exc: Исключение StarletteHttpException.
        :return: JSON-ответ с информацией об HTTP-ошибке.
        """
        if exc.status_code == HTTP_401_UNAUTHORIZED:
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorResponseSchema(
                    code=ResponseCodeEnum.UNAUTHORIZED_EXCEPTION,
                    numeric_code=exc.status_code,
                    detail=(
                        exc.detail if isinstance(exc.detail, str) else str(exc.detail)
                    ),
                ).model_dump(),
            )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """
        Обработчик необработанных исключений (500 Internal Server Error).

        :param request: Объект запроса.
        :param exc: Неизвестное исключение.
        :return: JSON-ответ с сообщением о внутренней ошибке сервера.
        """
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponseSchema(
                code=ResponseCodeEnum.INTERNAL_SERVER_ERROR,
                numeric_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера",
            ).model_dump(),
        )
