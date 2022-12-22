from datetime import datetime
from pydantic import BaseModel


class DetectionsBase(BaseModel):
    description: str | None
    creator_id: int


class DetectionsCreate(DetectionsBase):
    pass


class Detections(DetectionsBase):
    id: int
    create_datetime: datetime

    class Config:
        orm_mode = True
