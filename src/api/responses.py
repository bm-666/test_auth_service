from custom_types.types import ErrorResponseSchema, SuccessResponseSchema
from schemas.jwt_token import TokenSchema
from schemas.user import UserRead

common_400 = {400: {"description": "Некоректные данные", "model": ErrorResponseSchema}}

common_401 = {
    401: {
        "description": "Неавторизован или неверный токен",
        "model": ErrorResponseSchema,
    }
}

common_403 = {
    403: {
        "description": "Доступ запрещён",
        "model": ErrorResponseSchema,
    }
}

common_404 = {
    404: {
        "description": "Ресурс не найден",
        "model": ErrorResponseSchema,
    }
}

common_500 = {
    500: {
        "description": "Внутренняя ошибка сервера",
        "model": ErrorResponseSchema,
    }
}

# Ответы при регистрации
register_user_responses = {
    201: {
        "description": "Пользователь успешно зарегистрирован",
        "model": SuccessResponseSchema[UserRead],
    },
    **common_400,
    **common_500,
}

# Ответы при логине
login_responses = {
    200: {
        "description": "Успешная аутентификация. Возвращает JWT токен.",
        "model": SuccessResponseSchema[TokenSchema],
    },
    **common_400,
    **common_401,
    **common_500,
}

# Поулчения текущего пользователя
get_current_user_responses = {
    200: {
        "description": "Информация о текущем пользователе",
        "model": SuccessResponseSchema[UserRead],
    },
    **common_401,
    **common_403,
    **common_500,
}
