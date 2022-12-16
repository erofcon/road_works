from pydantic import BaseModel


class TaskImagesBase(BaseModel):
    url: str
    task_id: int


class TaskImagesCreate(TaskImagesBase):
    pass


class TaskImages(TaskImagesBase):
    id: int

    class Config:
        orm_mode = True
