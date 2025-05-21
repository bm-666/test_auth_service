from typing import Generic, TypeVar

from pydantic import BaseModel, EmailStr

from enums.enums import ResponseCodeEnum, TaskStatusEnum

T = TypeVar("T")  # тип модели для Response возврщаюших объект модели.


class EmailNotificationTask(BaseModel):
    to: EmailStr
    subject: str
    body: str


class TaskSchema(BaseModel):
    status: TaskStatusEnum = TaskStatusEnum.NEW
    data: dict


class BaseResponseSchema(BaseModel):
    code: ResponseCodeEnum
    numeric_code: int


class SuccessResponseSchema(BaseResponseSchema, Generic[T]):
    data: T | None = None


class ErrorResponseSchema(BaseResponseSchema):
    detail: str
