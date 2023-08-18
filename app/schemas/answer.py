from datetime import datetime

from pydantic import BaseModel


class AnswerBase(BaseModel):
    description: str | None
    task_id: int


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    create_id: int

    class Config:
        orm_mode = True


class AnswerQuery(BaseModel):
    id: int
    description: str | None
    create_datetime: datetime | None
    creator: dict | None
    answer_images: list | None
