from datetime import datetime

from pydantic import BaseModel


class AnswersBase(BaseModel):
    description: str | None
    task_id: int


class AnswersCreate(AnswersBase):
    pass


class Answers(AnswersBase):
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

    # create_id: int
    # task_id: int
    # description: str | None
    # answer_creator: dict | None
    # answer_images: list | None

# "id": 1,
#   "description": "hfkjsdnfmk -",
#   "create_datetime": "2023-01-09T10:57:34.707633",
#   "task_id": 1,
#   "creator_id": 1
