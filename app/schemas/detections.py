from datetime import datetime
from pydantic import BaseModel


class DetectionsBase(BaseModel):
    descriptions: str | None
    creator_id: int | None


class DetectionsCreate(DetectionsBase):
    pass


class Detections(DetectionsBase):
    id: int
    create_datetime: datetime

    class Config:
        orm_mode = True


class DetectionsWithUserName(Detections):
    username: str
