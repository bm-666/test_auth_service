from fastapi import APIRouter, Body
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from custom_types.types import SuccessResponseSchema
from database.session import get_async_session
from enums.enums import ResponseCodeEnum
from schemas.jwt_token import TokenSchema
from schemas.user import UserCreate, UserRead
from services.auth_services import AuthService

from ..responses import login_responses, register_user_responses

auth_routers = APIRouter(prefix="/auth", tags=["auth"])


@auth_routers.post(
    "/register",
    status_code=HTTP_201_CREATED,
    response_model=SuccessResponseSchema[UserRead],
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя.",
    responses=register_user_responses,
)
async def register(
    user: UserCreate = Body(), session: AsyncSession = Depends(get_async_session)
) -> SuccessResponseSchema[UserRead]:

    auth_service = AuthService(session=session)
    result = await auth_service.register_user(user)

    return SuccessResponseSchema(
        code=ResponseCodeEnum.SUCCESS,
        numeric_code=HTTP_201_CREATED,
        data=UserRead.model_validate(result).model_dump(),
    )


@auth_routers.post(
    "/login",
    response_model=SuccessResponseSchema[TokenSchema],
    summary="Аутентификация пользователя",
    description="Проверяет email и пароль пользователя. В случае успеха возвращает JWT токен",
    responses=login_responses,
)
async def login(
    user: UserCreate = Body(), session: AsyncSession = Depends(get_async_session)
) -> None:
    auth_services = AuthService(session=session)
    print("Hello")
    jwt_token = await auth_services.authenticate_user(
        email=user.email, password=user.password
    )
    return SuccessResponseSchema(
        code=ResponseCodeEnum.SUCCESS,
        numeric_code=HTTP_200_OK,
        data=jwt_token.model_dump(),
    )
