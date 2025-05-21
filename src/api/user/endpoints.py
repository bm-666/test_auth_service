from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from custom_types.types import SuccessResponseSchema
from enums.enums import ResponseCodeEnum
from schemas.user import UserRead

from ..dependencies import get_current_user
from ..responses import get_current_user_responses

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get(
    "/me",
    status_code=HTTP_200_OK,
    response_model=SuccessResponseSchema[UserRead],
    summary="Получение текущего пользователя",
    description="Возвращает данные пользователя, извлечённого из JWT-токена. "
    "Требуется передать токен в заголовке Authorization.",
    responses=get_current_user_responses,
)
async def user_info(
    user: UserRead = Depends(get_current_user),
) -> SuccessResponseSchema[UserRead]:
    return SuccessResponseSchema(
        code=ResponseCodeEnum.SUCCESS,
        numeric_code=HTTP_200_OK,
        data=UserRead.model_validate(user).model_dump(),
    )
