from pydantic import BaseModel, ConfigDict

from enums.enums import TaskStatusEnum


class TaskCreate(BaseModel):
    """
    Схема для создания новой задачи.

    :param status: Статус задачи. По умолчанию — NEW.
    :param data: Словарь с данными, необходимыми для выполнения задачи.
    """

    status: TaskStatusEnum = TaskStatusEnum.NEW
    data: dict


class TaskRead(TaskCreate):
    """
    Схема для чтения задачи, включая её уникальный идентификатор.

    :param id: Уникальный идентификатор задачи.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
