from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    description: str | None
    lead_datetime: datetime
    latitude: float | None
    longitude: float | None
    executor_id: int
    group_id: int


class CreateTask(TaskBase):
    pass


class Task(TaskBase):
    id: int
    create_datetime: datetime
    is_done: bool
    creator_id: int

    class Config:
        orm_mode = True


class CurrentTask(BaseModel):
    id: int
    description: str | None
    create_datetime: datetime | None
    creator_id: int | None
    executor_id: int | None
    creator_username: str | None
    executor_username: str | None
    task_status: str | None

    class Config:
        orm_mode = True


class TaskQuery(BaseModel):
    id: int
    description: str | None
    create_datetime: datetime | None
    lead_datetime: datetime | None
    latitude: float | None
    longitude: float | None
    task_status: str
    group_id: int | None
    group_name: str | None
    task_images: list | None
    task_creator: dict | None
    task_executor: dict | None
