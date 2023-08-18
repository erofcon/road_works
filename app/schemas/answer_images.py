from pydantic import BaseModel


class AnswerImagesBase(BaseModel):
    url: str
    answer_id: int


class AnswerImagesCreate(AnswerImagesBase):
    pass


class AnswerImages(AnswerImagesBase):
    id: int

    class Config:
        orm_mode = True
