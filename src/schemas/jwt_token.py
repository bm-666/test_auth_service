from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Модель JWT-токена доступа.
    Используется для передачи токена авторизации клиенту после успешного входа в систему.
    """

    access_token: str
    token_type: str
