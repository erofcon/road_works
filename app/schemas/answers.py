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
