from enum import StrEnum


class TaskStatusEnum(StrEnum):
    SEND = "SEND"
    FAILED = "FAILED"
    NEW = "NEW"


class TaskTypeEnum(StrEnum):
    EMAIL = "email"


class ServiceEnum(StrEnum):
    API = "api"
    WORKER = "worker"
    NOTIFICATION = "notification"


class QueueEnum(StrEnum):
    EMAIL = "email"


class ResponseCodeEnum(StrEnum):
    SUCCESS = "SUCCESS"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    UNAUTHORIZED_EXCEPTION = "UNAUTHORIZED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    HTTP_ERROR = "HTTP_ERROR"
    FORBIDDEN = "FORBIDDEN"


class EmailSubjectEnum(StrEnum):
    REGISTRATION = "Registration"
