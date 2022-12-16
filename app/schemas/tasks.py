from datetime import datetime

from pydantic import BaseModel


class TasksBase(BaseModel):
    description: str | None
    lead_datetime: datetime
    latitude: float | None
    longitude: float | None
    executor_id: int
    group_id: int


class CreateTask(TasksBase):
    pass


class Tasks(TasksBase):
    id: int
    create_datetime: datetime
    is_done: bool
    creator_id: int

    class Config:
        orm_mode = True


class CurrentTasks(BaseModel):
    id: int
    description: str | None
    create_datetime: datetime | None
    lead_datetime: datetime | None
    latitude: float | None
    longitude: float | None
    creator_id: int | None
    executor_id: int | None
    task_status: str
